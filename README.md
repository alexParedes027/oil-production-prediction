# Predicción de producción de petróleo en pozos no convencionales

Proyecto final del curso **EnergIA Digital – Data Science** de Fundación YPF.

**Grupo:** 6

**Integrantes:**

- Alex Paredes
- Julián Varela

---

## Objetivo del proyecto

El objetivo es analizar la producción de petróleo de pozos no convencionales de Argentina y desarrollar modelos de Machine Learning para estimar su comportamiento productivo.

La pregunta principal que buscamos responder es:

> **Dadas las características de un pozo y su historial de producción, ¿cuánto petróleo esperamos que produzca el próximo mes?**

El enfoque principal del proyecto es la **regresión**, ya que permite estimar directamente el volumen de producción esperado en metros cúbicos. Como complemento, también desarrollamos un modelo de **clasificación** para categorizar la producción futura en niveles bajo, medio y alto.

---

## Fuentes de datos

Los datos utilizados provienen de [Datos Argentina](https://www.datos.gob.ar/datasetproduccion-de-petroleo-y-gas-por-pozo), el portal oficial de datos abiertos del Gobierno de la República Argentina.

Se utilizaron tres fuentes principales:

- `produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv`: contiene registros mensuales de producción de petróleo, gas, agua y otras variables operativas por pozo.
- `capitulo-iv-pozos.csv`: contiene características generales de los pozos, como ubicación, profundidad, formación, cuenca, tipo de recurso y tipo de extracción.
- `datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv`: contiene información relacionada con las operaciones de fracturación y terminación de los pozos.

El identificador utilizado para relacionar las distintas fuentes es `idpozo`.

Los archivos originales se descargaron y se mantienen localmente. La carpeta compartida del equipo se utilizó únicamente como medio de distribución entre los integrantes.

---

## Estructura del repositorio

```text
oil-production-prediction/
│
├── data/
│   ├── raw/                              # Datos originales, sin modificar
│   └── processed/                        # Datos procesados y datasets de modelado
│
├── notebooks/
│   ├── 01_exploracion_datos.ipynb
│   ├── 02_preprocesamiento.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modelado_regresion.ipynb
│   └── 05_modelado_clasificacion.ipynb
│
├── src/                                  # Código reutilizable del proyecto
├── reports/                              # Gráficos, resultados y material de presentación
│
├── descargar_datos.py                   # Descarga de los datasets
├── requirements.txt                      # Dependencias del proyecto
├── .gitignore
└── README.md

```
