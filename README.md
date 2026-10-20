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
├── README.md
└── README2.md
```

Los archivos originales no se incluyen en el repositorio debido a su tamaño. Para reproducir el análisis, deben descargarse y ubicarse dentro de `data/raw/`.

---

## Flujo de trabajo

### 1. Exploración de datos

En `01_exploracion_datos.ipynb` se realizó el análisis exploratorio inicial de las fuentes de datos.

Se trabajó sobre:

- Dimensiones de los datasets;
- Nombres y tipos de variables;
- Valores faltantes;
- Registros duplicados;
- Granularidad de cada fuente;
- Períodos temporales disponibles;
- Distribución de la producción;
- Comportamiento de los pozos según su tipo;
- Características de las formaciones y cuencas;
- Posibles valores inconsistentes o extremos;
- Relación entre producción, características del pozo y fracturación.

El análisis exploratorio permitió conocer la estructura de los datos y tomar decisiones para las etapas posteriores. Entre los aspectos observados se encontraron valores faltantes, distribuciones sesgadas, valores extremos y diferencias importantes entre distintos tipos de pozos y períodos históricos.

También se identificó que la producción presenta una fuerte variabilidad entre pozos y que no todas las fuentes tienen la misma granularidad. Por este motivo, antes de realizar los cruces fue necesario revisar la unicidad de las claves y el nivel de detalle de cada archivo.

### 2. Preprocesamiento e integración

En `02_preprocesamiento.ipynb` se realizó la limpieza y preparación de las fuentes.

Las principales tareas fueron:

- Tratamiento de valores inconsistentes;
- Revisión y normalización de fechas;
- Corrección de variables de producción y operación;
- Tratamiento de duplicados;
- Integración de las fuentes mediante `idpozo`;
- Preparación de la información de fracturación;
- Construcción de una tabla mensual por pozo;
- Creación del objetivo de producción del mes siguiente.

La unidad principal de análisis quedó definida como un registro correspondiente a un pozo en un determinado mes.

El objetivo de regresión se definió como:

```text
prod_pet_mes_siguiente
```

Esta variable representa la producción de petróleo del mismo pozo durante el mes siguiente al mes de corte.

### 3. Ingeniería de variables y partición temporal

En `03_feature_engineering.ipynb` se construyeron las variables predictoras que representan el historial del pozo y la información disponible al cierre de cada mes.

Se generaron, entre otras:

- Producción del mes de corte;
- Rezagos de producción;
- Medias móviles;
- Desvíos de producción;
- Cambios absolutos y relativos;
- Producción acumulada;
- Producción por día;
- Meses desde el inicio del pozo;
- Variables de fracturación;
- Variables operativas;
- Características geográficas y geológicas;
- Variables categóricas del pozo.

La variable de clasificación se definió como:

```text
clase_prod_pet_mes_siguiente
```

Esta variable categoriza la producción futura en tres niveles:

- `Baja`;
- `Media`;
- `Alta`.

Para evitar mezclar información del futuro con el pasado, se utilizaron particiones temporales:

- **Entrenamiento:** objetivos de febrero a diciembre de 2025.
- **Validación:** objetivos de enero a marzo de 2026.
- **Test:** objetivos de abril a julio de 2026.
- **Inferencia:** información disponible hasta julio de 2026 para predecir agosto de 2026.

Las variables históricas se calcularon utilizando la información temporal disponible para cada pozo. Además, se generó un archivo histórico adicional para evaluar si ampliar la ventana de entrenamiento con objetivos desde 2020 mejoraba el desempeño.

---

## Modelado de regresión

En `04_modelado_regresion.ipynb` se desarrolló el modelo principal del proyecto.

El objetivo es predecir la cantidad de petróleo que producirá cada pozo durante el mes siguiente, expresada en metros cúbicos.

### Modelos evaluados

Se compararon:

- Modelo de persistencia;
- Random Forest Regressor;
- Ridge;
- Estrategia de dos etapas basada en clasificación y regresión.

El modelo de persistencia se utilizó como referencia. Este modelo supone que la producción del próximo mes será igual a la producción del mes de corte.

También se realizó validación temporal mediante distintos pliegues y se compararon configuraciones del Random Forest modificando algunos hiperparámetros, entre ellos:

- `min_samples_leaf`;
- `max_features`.

### Comparación de ventanas de entrenamiento

Inicialmente, el modelo se entrenaba utilizando objetivos desde 2025. Luego se evaluó si incorporar objetivos desde 2020 mejoraba los resultados.

La comparación se realizó manteniendo constantes:

- Las variables predictoras;
- El algoritmo;
- Los hiperparámetros;
- Los períodos de validación;
- Las métricas de evaluación.

La ventana desde 2020 obtuvo una mejora moderada y consistente respecto de la ventana desde 2025. Por este motivo, se seleccionó como ventana final el período comprendido entre enero de 2020 y diciembre de 2025.

Los objetivos anteriores a 2020 no se utilizaron como ejemplos directos de entrenamiento. Sin embargo, esos años pueden aportar información histórica para construir variables como la producción acumulada, los rezagos y la antigüedad de los pozos.

### Resultado final de regresión

El modelo seleccionado fue un **Random Forest Regressor** entrenado con objetivos desde enero de 2020 hasta diciembre de 2025.

En el conjunto de test obtuvo:

| Modelo              | MAE (m³) | RMSE (m³) |    R² |
| ------------------- | -------: | --------: | ----: |
| Persistencia        |  166,195 |   551,710 | 0,820 |
| Random Forest final |  133,039 |   393,443 | 0,908 |

El modelo final:

- Redujo aproximadamente un 20 % el MAE respecto de la persistencia;
- Redujo aproximadamente un 29 % el RMSE;
- Obtuvo un R² de 0,908;
- No generó predicciones negativas.

El análisis por grupos mostró que el modelo obtiene mejores resultados en los registros con producción positiva. En los registros cuya producción real fue igual a cero se observó una leve tendencia a sobreestimar, aunque el error se mantuvo considerablemente menor que en los casos de producción positiva.

### Inferencia de producción para agosto de 2026

Una vez entrenado y evaluado el modelo final, se utilizó el conjunto de inferencia correspondiente a julio de 2026.

Cada fila de ese conjunto representa la situación de un pozo con la información disponible hasta julio de 2026. El modelo utiliza esas variables para estimar la producción de petróleo del mismo pozo durante agosto de 2026.

Se generaron predicciones para:

- 5.062 registros;
- 5.062 pozos;
- mes de corte: julio de 2026;
- mes objetivo: agosto de 2026.

El archivo generado es:

```text
data/processed/predicciones_produccion_agosto_2026.csv
```

Como todavía no se conoce la producción real de agosto de 2026, estas predicciones no pueden evaluarse mediante MAE, RMSE o R².

---

## Modelado de clasificación

En `05_modelado_clasificacion.ipynb` se desarrolló un modelo complementario de clasificación multiclase.

El objetivo es categorizar la producción futura como:

- `Baja`;
- `Media`;
- `Alta`.

La clasificación no busca estimar el volumen exacto en metros cúbicos. Su objetivo es brindar una interpretación más general del nivel de producción esperado.

### Modelo de referencia

Como referencia se utilizó un modelo que siempre predice la clase mayoritaria del conjunto de entrenamiento.

En validación obtuvo:

- accuracy: 0,353;
- balanced accuracy: 0,333;
- F1 macro: 0,174.

### Clasificador seleccionado

Se entrenó un **Random Forest Classifier** utilizando las mismas variables predictoras principales que en la regresión.

También se realizó una comparación breve de hiperparámetros mediante el ajuste de `max_features`. La configuración seleccionada utilizó:

```text
max_features = 0,7
```

### Resultado final de clasificación

En el conjunto de test, el clasificador obtuvo:

| Métrica           | Resultado |
| ----------------- | --------: |
| Accuracy          |     0,935 |
| Balanced accuracy |     0,932 |
| Precision macro   |     0,933 |
| Recall macro      |     0,932 |
| F1 macro          |     0,933 |

El desempeño fue similar al observado en validación, lo que indica que el modelo conserva un comportamiento estable al evaluarse sobre meses posteriores.

La clase `Media` presentó mayores dificultades que `Baja` y `Alta`, principalmente porque representa una categoría intermedia y puede confundirse con las clases vecinas.

La clasificación se presenta como un complemento del modelo de regresión. La regresión responde directamente a la pregunta principal del proyecto —cuánto se espera producir—, mientras que la clasificación resume esa producción en niveles más fáciles de interpretar.

### Inferencia de categorías para agosto de 2026

También se puede aplicar el clasificador final al conjunto de inferencia correspondiente a julio de 2026 para obtener una categoría estimada de producción para agosto de 2026.

El archivo generado es:

```text
data/processed/predicciones_clasificacion_agosto_2026.csv
```

Estas categorías no pueden evaluarse todavía porque no se conoce la producción real de agosto de 2026.

---

## Resultados y conclusiones

El desarrollo realizado permitió completar un flujo de aprendizaje supervisado desde la exploración inicial hasta la evaluación de los modelos.

El modelo principal de regresión:

- Utiliza información histórica y características de los pozos;
- Respeta el orden temporal de los datos;
- Supera a la referencia de persistencia;
- Fue evaluado mediante validación y test;
- Permite generar estimaciones de producción para un mes futuro.

El modelo complementario de clasificación:

- Distingue entre niveles bajo, medio y alto de producción;
- Supera ampliamente a la referencia de clase mayoritaria;
- Presenta un desempeño equilibrado entre las tres categorías;
- Permite resumir la predicción de manera más sencilla.

Los resultados muestran que el modelo puede encontrar patrones útiles en el historial productivo y en las características de los pozos. Sin embargo, las predicciones no deben interpretarse como valores exactos para todos los casos. Los errores son mayores en algunos pozos de producción elevada y en situaciones donde la producción futura presenta variaciones difíciles de anticipar.

---

## Estado actual del proyecto

Actualmente se encuentran completadas las siguientes etapas:

- Exploración y análisis de los datos;
- Limpieza y preprocesamiento;
- Integración de las fuentes;
- Ingeniería de variables;
- Definición del objetivo temporal;
- Partición cronológica de los datos;
- Modelo supervisado de regresión;
- Modelo supervisado de clasificación;
- Ajuste básico de hiperparámetros;
- Validación temporal;
- Evaluación en el conjunto de test;
- Análisis de errores;
- Inferencia de producción y categorías para agosto de 2026.

Como posibles etapas posteriores quedan:

1. Desarrollar un modelo de clustering a partir de las variables seleccionadas;
2. Justificar la elección del algoritmo y de las variables utilizadas;
3. Analizar y mejorar los grupos obtenidos según un criterio explícito;
4. Comparar los perfiles de pozos identificados;
5. Preparar el storytelling y la presentación oral final;
6. Documentar las conclusiones generales del proyecto.

---

## Instalación y ejecución

Se recomienda utilizar Python 3.11 o una versión compatible.

### Crear el entorno virtual

```bash
python -m venv .venv
```

### Activar el entorno en Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Instalar las dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Descargar los datos

Si los archivos no se encuentran disponibles localmente, pueden descargarse utilizando:

```powershell
python descargar_datos.py
```

El script guarda los archivos dentro de `data/raw/` y evita volver a descargar aquellos que ya existen.

Para ejecutar las notebooks desde Visual Studio Code, se debe seleccionar el entorno `.venv` como kernel de Python.

---

## Nota metodológica

Las particiones se realizaron respetando el orden temporal para evitar utilizar información futura durante el entrenamiento.

El preprocesamiento y las transformaciones se ajustan utilizando los datos de entrenamiento. La validación se utiliza para comparar modelos y configuraciones, mientras que el conjunto de test se reserva para informar el desempeño final.

La inferencia para agosto de 2026 se realiza utilizando las variables disponibles hasta julio de 2026. Como todavía no se conoce la producción real de agosto, esas predicciones no cuentan aún con una evaluación mediante métricas.
