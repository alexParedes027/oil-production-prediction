"""Funciones compartidas por las notebooks de exploración.

Reutilizan los archivos generados por las notebooks 01 a 03 del proyecto
(`data/processed`) y la misma configuración de Random Forest que la
notebook 04, entrenada con los últimos 24 meses de objetivos.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

RUTA_EXPLORACION = Path(__file__).resolve().parent
RUTA_DATOS = RUTA_EXPLORACION.parent / "data" / "processed"
RUTA_RESULTADOS = RUTA_EXPLORACION / "resultados"
RUTA_RESULTADOS.mkdir(exist_ok=True)

VENTANA_MESES = 24
MESES_CONTEO_NUEVOS = 6
VENTANA_CURVA = 12

with open(RUTA_DATOS / "columnas_modelado.json", encoding="utf-8") as archivo:
    _definicion = json.load(archivo)

FEATURES_NUMERICAS = _definicion["features_numericas"] + _definicion["features_booleanas"]
FEATURES_CATEGORICAS = _definicion["features_categoricas"]
FEATURES = FEATURES_NUMERICAS + FEATURES_CATEGORICAS
OBJETIVO = _definicion["target_regresion"]


def sumar_meses(fechas, meses):
    """Suma meses a una serie de fechas que corresponden al primer día del mes."""
    return (fechas.dt.to_period("M") + meses).dt.to_timestamp()


def crear_modelo(n_estimators=200):
    """Random Forest con la configuración final de la notebook 04."""
    preprocesamiento = ColumnTransformer([
        ("numericas", SimpleImputer(strategy="median", add_indicator=True), FEATURES_NUMERICAS),
        ("categoricas", Pipeline([
            ("imputacion", SimpleImputer(strategy="constant", fill_value="Sin dato")),
            ("one_hot", OneHotEncoder(handle_unknown="ignore", min_frequency=20)),
        ]), FEATURES_CATEGORICAS),
    ])
    modelo = RandomForestRegressor(
        n_estimators=n_estimators,
        min_samples_leaf=5,
        max_depth=None,
        max_features=0.7,
        random_state=42,
        n_jobs=-1,
    )
    return Pipeline([("preprocesamiento", preprocesamiento), ("modelo", modelo)])


def cargar_panel():
    """Une todos los registros con objetivo conocido (2006-02 a 2026-07).

    Devuelve el panel con objetivo y el conjunto de inferencia (julio 2026).
    """
    columnas = ["idpozo", "sigla", "fecha", "mes_objetivo"] + FEATURES + [OBJETIVO]
    leer = lambda nombre, cols: pd.read_csv(
        RUTA_DATOS / nombre, usecols=cols, parse_dates=["fecha", "mes_objetivo"], low_memory=False
    )
    historico = leer("entrenamiento_historico_candidato.csv", columnas)
    validacion = leer("validation_modelado.csv", columnas)
    test = leer("test_modelado.csv", columnas)
    assert historico["mes_objetivo"].max() < validacion["mes_objetivo"].min()

    panel = pd.concat([historico, validacion, test], ignore_index=True)
    assert not panel.duplicated(["idpozo", "fecha"]).any()

    inferencia = leer("inferencia_modelado.csv", columnas[:-1])
    return panel, inferencia


def agregar_objetivo_horizonte(panel, horizonte):
    """Agrega la producción del pozo `horizonte` meses después del mes de corte.

    Para horizonte=1 coincide con el objetivo original. Se conservan solo los
    pozos que siguen informando producción en el mes objetivo.
    """
    produccion = panel[["idpozo", "mes_objetivo", OBJETIVO]].rename(
        columns={"mes_objetivo": "mes_objetivo_h", OBJETIVO: "objetivo_h"}
    )
    datos = panel.assign(mes_objetivo_h=sumar_meses(panel["fecha"], horizonte))
    return datos.merge(produccion, on=["idpozo", "mes_objetivo_h"], how="inner", validate="one_to_one")


def cargar_produccion_pais():
    """Producción mensual de petróleo por pozo, con el primer mes registrado del pozo."""
    produccion = pd.read_csv(
        RUTA_DATOS / "produccion_limpio.csv",
        usecols=["anio", "mes", "idpozo", "prod_pet", "empresa"],
        low_memory=False,
    )
    produccion["fecha"] = pd.to_datetime(dict(year=produccion["anio"], month=produccion["mes"], day=1))
    produccion["primer_mes"] = produccion.groupby("idpozo")["fecha"].transform("min")
    produccion["mes_de_vida"] = (
        (produccion["fecha"].dt.year - produccion["primer_mes"].dt.year) * 12
        + produccion["fecha"].dt.month - produccion["primer_mes"].dt.month + 1
    )
    return produccion.drop(columns=["anio", "mes"])


def resumen_pozos_nuevos(produccion):
    """Por mes: producción total, pozos que aparecen por primera vez y su petróleo."""
    nuevos = produccion[produccion["mes_de_vida"] == 1]
    resumen = pd.DataFrame({
        "total_pais_m3": produccion.groupby("fecha")["prod_pet"].sum(),
        "pozos_nuevos": nuevos.groupby("fecha").size(),
        "petroleo_pozos_nuevos_m3": nuevos.groupby("fecha")["prod_pet"].sum(),
    }).fillna(0)
    resumen.index.name = "mes"
    return resumen


def curva_tipo(produccion, mes_corte, meses_vida=12, ventana=VENTANA_MESES):
    """Producción media por mes de vida de los pozos que empezaron en la ventana.

    Solo usa información disponible hasta `mes_corte`. Un pozo que no informa
    en un mes de su vida cuenta como cero en ese mes.
    """
    mes_corte = pd.Timestamp(mes_corte)
    inicio = mes_corte - pd.DateOffset(months=ventana - 1)
    conocidos = produccion[produccion["fecha"] <= mes_corte]
    primer_mes = conocidos.groupby("idpozo")["primer_mes"].first()
    cohorte = primer_mes[(primer_mes >= inicio) & (primer_mes <= mes_corte)]

    curva = {}
    for mes_vida in range(1, meses_vida + 1):
        # Pozos que ya tuvieron tiempo de llegar a este mes de vida.
        elegibles = cohorte[cohorte + pd.DateOffset(months=mes_vida - 1) <= mes_corte].index
        if len(elegibles) == 0:
            break
        en_mes = conocidos[conocidos["idpozo"].isin(elegibles) & (conocidos["mes_de_vida"] == mes_vida)]
        curva[mes_vida] = en_mes["prod_pet"].sum() / len(elegibles)
    return pd.Series(curva, name="m3_por_pozo")


def pronostico_pozos_nuevos(
    produccion, resumen, mes_corte, horizonte,
    meses_conteo=MESES_CONTEO_NUEVOS, ventana_curva=VENTANA_CURVA, ajustar_tendencia=True,
):
    """Petróleo esperado en `mes_corte + horizonte` de los pozos que se conecten después del corte.

    Supone que se conectan tantos pozos por mes como el promedio de los últimos
    `meses_conteo` meses y que cada uno produce según la curva tipo de los pozos
    que empezaron en los últimos `ventana_curva` meses.

    Con `ajustar_tendencia`, la curva se corrige por la mejora anual de los pozos
    nuevos: los pozos de la ventana empezaron, en promedio, `ventana_curva / 2`
    meses antes del corte, y los que se conecten después son más nuevos.
    """
    mes_corte = pd.Timestamp(mes_corte)
    historia = resumen.loc[:mes_corte].tail(meses_conteo)
    pozos_por_mes = historia["pozos_nuevos"].mean()
    curva = curva_tipo(produccion, mes_corte, meses_vida=horizonte, ventana=ventana_curva).loc[1:horizonte]
    if ajustar_tendencia:
        curva_anio_anterior = curva_tipo(
            produccion, mes_corte - pd.DateOffset(months=12), meses_vida=horizonte, ventana=ventana_curva
        ).loc[1:horizonte]
        mejora_anual = curva.sum() / curva_anio_anterior.sum()
        curva = curva * mejora_anual ** (ventana_curva / 2 / 12)
    return pozos_por_mes * curva.sum(), pozos_por_mes


def petroleo_conectados_despues(produccion, mes_corte, mes_objetivo):
    """Petróleo real en `mes_objetivo` de los pozos cuyo primer mes es posterior al corte."""
    en_mes = produccion[produccion["fecha"] == pd.Timestamp(mes_objetivo)]
    return en_mes.loc[en_mes["primer_mes"] > pd.Timestamp(mes_corte), "prod_pet"].sum()


def backtest_rodante(panel, horizonte, meses_objetivo, ventana=VENTANA_MESES, verbose=True, usar_cache=True):
    """Pronostica cada mes objetivo usando solo información disponible al mes de corte.

    Para cada mes objetivo T, el mes de corte es T - horizonte. El modelo se
    entrena con los objetivos de los `ventana` meses que terminan en el corte.
    """
    import time

    meses_objetivo = pd.to_datetime(meses_objetivo)
    ruta_cache = RUTA_RESULTADOS / "cache" / (
        f"rodante_h{horizonte}_{meses_objetivo.min():%Y%m}_{meses_objetivo.max():%Y%m}_v{ventana}.csv"
    )
    if usar_cache and ruta_cache.exists():
        print(f"Usando resultados guardados: {ruta_cache.name}")
        return pd.read_csv(ruta_cache, parse_dates=["mes_corte", "mes_objetivo"])

    datos = agregar_objetivo_horizonte(panel, horizonte)
    filas = []
    for mes_objetivo in meses_objetivo:
        mes_corte = mes_objetivo - pd.DateOffset(months=horizonte)
        inicio_ventana = mes_corte - pd.DateOffset(months=ventana - 1)
        entrenamiento = datos[datos["mes_objetivo_h"].between(inicio_ventana, mes_corte)]
        evaluacion = datos[datos["fecha"] == mes_corte]
        assert (evaluacion["mes_objetivo_h"] == mes_objetivo).all()

        inicio = time.time()
        modelo = crear_modelo().fit(entrenamiento[FEATURES], entrenamiento["objetivo_h"])
        prediccion = np.clip(modelo.predict(evaluacion[FEATURES]), 0, None)

        real = evaluacion["objetivo_h"].to_numpy()
        persistencia = evaluacion["prod_pet"].to_numpy()
        filas.append({
            "horizonte": horizonte,
            "mes_corte": mes_corte,
            "mes_objetivo": mes_objetivo,
            "pozos": len(evaluacion),
            "filas_entrenamiento": len(entrenamiento),
            "real_existentes_m3": real.sum(),
            "pronostico_existentes_m3": prediccion.sum(),
            "persistencia_existentes_m3": persistencia.sum(),
            "mae_modelo": np.abs(prediccion - real).mean(),
            "mae_persistencia": np.abs(persistencia - real).mean(),
        })
        if verbose:
            print(
                f"h={horizonte} corte {mes_corte:%Y-%m} -> {mes_objetivo:%Y-%m}: "
                f"{len(entrenamiento):,} filas, {time.time() - inicio:.0f} s"
            )
    resultado = pd.DataFrame(filas)
    ruta_cache.parent.mkdir(exist_ok=True)
    resultado.to_csv(ruta_cache, index=False)
    return resultado


def pronostico_desde_julio(panel, inferencia, horizonte, ventana=VENTANA_MESES):
    """Entrena con los últimos `ventana` meses conocidos y pronostica desde julio de 2026."""
    datos = agregar_objetivo_horizonte(panel, horizonte)
    mes_corte = inferencia["fecha"].max()
    inicio_ventana = mes_corte - pd.DateOffset(months=ventana - 1)
    entrenamiento = datos[datos["mes_objetivo_h"].between(inicio_ventana, mes_corte)]
    modelo = crear_modelo().fit(entrenamiento[FEATURES], entrenamiento["objetivo_h"])
    resultado = inferencia[["idpozo", "sigla", "empresa", "prod_pet"]].copy()
    resultado["mes_objetivo"] = mes_corte + pd.DateOffset(months=horizonte)
    resultado["produccion_predicha_m3"] = np.clip(modelo.predict(inferencia[FEATURES]), 0, None)
    return resultado, entrenamiento
