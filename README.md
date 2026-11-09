# Predicción de producción de petróleo en pozos no convencionales

Proyecto final del curso **EnergIA Digital – Data Science** de Fundación YPF.

**Grupo:** 6

**Integrantes:**

- **Alex Paredes**
- **Julián Varela**

## Resumen del proyecto

En este proyecto analizamos la producción de petróleo de pozos no convencionales de Argentina. Integramos información mensual de producción con características geológicas, operativas y de fracturación para estudiar el comportamiento de los pozos y construir modelos de Machine Learning. El trabajo incluye análisis exploratorio, preparación de datos, ingeniería de variables, modelos supervisados y un modelo no supervisado de clustering.

## Datos utilizados

Los datos fueron obtenidos del portal oficial [Datos Argentina](https://www.datos.gob.ar/datasetproduccion-de-petroleo-y-gas-por-pozo). Las fuentes principales fueron:

- `produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv`: Producción mensual de petróleo, gas, agua y otros indicadores por pozo.
- `capitulo-iv-pozos.csv`: Características generales de los pozos, como profundidad, formación, cuenca, provincia y tipo de extracción.
- `datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv`: Información relacionada con la fracturación y terminación de los pozos.

También se utilizaron archivos complementarios del mismo conjunto de datos para validar fechas e incorporar información histórica. Las fuentes se integraron mediante el identificador `idpozo`.

Los archivos originales son pesados y se mantienen fuera del control de versiones. Se pueden descargar mediante `descargar_datos.py` o copiar desde el ZIP compartido por el equipo dentro de `data/raw/`. Esta carpeta conserva los archivos originales sin modificar.

## Objetivo y preguntas de trabajo

La pregunta principal fue:

> **Dadas las características de un pozo y su historial de producción, ¿cuánto petróleo esperamos que produzca durante el próximo mes?**

Para responderla trabajamos con tres enfoques:

- **Regresión:** Predecir la producción de petróleo del mes siguiente en metros cúbicos.
- **Clasificación:** Categorizar la producción futura en niveles bajo, medio y alto.
- **Clustering:** Identificar perfiles de pozos con características productivas y operativas similares.

Además de predecir, buscamos comprender qué variables se relacionan con el comportamiento productivo, qué diferencias existen entre los pozos y qué decisiones metodológicas permiten construir modelos confiables.

## Flujo general de trabajo

El proyecto se desarrolló en las siguientes etapas:

1. Exploración de las fuentes y comprensión de la estructura de los datos.
2. Limpieza, validación e integración mediante `idpozo`.
3. Construcción de una tabla mensual integrada por pozo.
4. Ingeniería de variables históricas y temporales.
5. Definición del objetivo de producción del mes siguiente.
6. Entrenamiento y evaluación de modelos de regresión y clasificación.
7. Construcción de perfiles agregados, uno por pozo, para clustering.
8. Aplicación, evaluación e interpretación de DBSCAN.
9. Análisis de resultados, limitaciones y conclusiones.

## 1. Análisis exploratorio de datos

En `01_exploracion_datos.ipynb` analizamos las fuentes originales con Pandas y visualizaciones estadísticas. Revisamos la cantidad de filas y columnas, los tipos de datos, los valores faltantes, los duplicados, los identificadores, la granularidad y los períodos disponibles.

También estudiamos la distribución de la producción y su relación con la cuenca, la provincia, la formación, el tipo de pozo y el sistema de extracción. El análisis mostró que las fuentes tenían distintos niveles de detalle y que la producción presentaba una distribución sesgada, con diferencias importantes entre pozos.

Estos resultados fueron importantes para decidir cómo integrar las fuentes, cómo tratar las variables y cómo evitar que los valores extremos o la información futura afectaran el modelado.

## 2. Limpieza, integración y preparación

En `02_preprocesamiento.ipynb` normalizamos fechas y nombres de variables, revisamos unidades, validamos identificadores, tratamos duplicados e integramos la información mediante `idpozo`. La unidad de análisis para los modelos supervisados quedó definida como un pozo observado en un mes determinado.

En `03_feature_engineering.ipynb` construimos variables utilizando únicamente la información disponible hasta cada mes de corte. Generamos rezagos, medias móviles, producción acumulada, cambios recientes, producción por día, meses desde el inicio e información operativa, geológica y de fracturación.

El objetivo `prod_pet_mes_siguiente` representa la producción de petróleo del mismo pozo durante el mes posterior al corte. Para evitar el uso de información futura, dividimos los datos cronológicamente:

- **Entrenamiento:** Enero de 2020 a diciembre de 2025.
- **Validación:** Enero a marzo de 2026.
- **Test:** Abril a julio de 2026.
- **Inferencia:** Información hasta julio de 2026 para estimar agosto de 2026.

Esta estrategia permite evaluar los modelos en un escenario más parecido al uso real.

## 3. Modelo supervisado de regresión

En `04_modelado_regresion.ipynb` comparamos un modelo de persistencia, Random Forest Regressor, Ridge y una estrategia de dos etapas basada en clasificación y regresión. La persistencia se utilizó como referencia y supone que la producción del próximo mes será igual a la del mes de corte.

El modelo final fue un **Random Forest Regressor**, porque superó la referencia en el conjunto de test:

| Modelo              | MAE (m³) | RMSE (m³) |    R² |
| ------------------- | -------: | --------: | ----: |
| Persistencia        |  166,195 |   551,710 | 0,820 |
| Random Forest final |  133,039 |   393,443 | 0,908 |

El modelo redujo aproximadamente un 20 % el MAE y un 29 % el RMSE respecto de la persistencia, y no produjo predicciones negativas. Luego se utilizó para estimar la producción de agosto de 2026 para 5.062 pozos. Esas predicciones no se evaluaron dentro de este trabajo porque el dataset utilizado llega hasta julio de 2026.

## 4. Modelo supervisado de clasificación

En `05_modelado_clasificacion.ipynb` transformamos el objetivo futuro en tres categorías: `Baja`, `Media` y `Alta`. Comparamos una referencia basada en la clase mayoritaria con un **Random Forest Classifier**.

El clasificador obtuvo los siguientes resultados en el conjunto de test:

| Métrica           | Resultado |
| ----------------- | --------: |
| Accuracy          |     0,935 |
| Balanced accuracy |     0,932 |
| Precision macro   |     0,933 |
| Recall macro      |     0,932 |
| F1 macro          |     0,933 |

Las métricas muestran un desempeño equilibrado entre las tres clases. La categoría `Media` fue la más difícil de distinguir porque se encuentra entre los niveles bajo y alto. También se generaron categorías estimadas para agosto de 2026, que no se evaluaron dentro del período disponible en este trabajo.

## 5. Modelo no supervisado de clustering

En `06_exploracion_clustering.ipynb` cambiamos la unidad de análisis: en lugar de trabajar con un registro mensual, construimos un perfil resumido por pozo. El dataset integrado contiene 421.046 registros mensuales y 5.089 pozos entre enero de 2006 y julio de 2026. Luego de conservar los pozos con al menos seis meses observados, quedaron 4.839 perfiles y 29 variables.

En `07_modelado_clustering.ipynb` aplicamos **DBSCAN** sobre 16 variables numéricas. Transformamos las variables productivas con `log1p` cuando correspondía y utilizamos `StandardScaler` para obtener una escala comparable. Elegimos DBSCAN porque no requiere definir previamente la cantidad de grupos y permite identificar perfiles atípicos como ruido.

Después de comparar distintas configuraciones, seleccionamos `eps = 1,2` y `min_samples = 24`. El modelo produjo cuatro clusters, 3.979 pozos asignados y 860 pozos identificados como ruido, equivalente a un 82,23 % agrupado y un 17,77 % de ruido.

El Cluster 0 reúne los perfiles con mayor producción media y continuidad, principalmente petrolíferos, asociados con Vaca Muerta y shale. Los Clusters 2 y 3 presentan producción petrolera casi nula, predominio de pozos gasíferos y una mayor proporción de recursos tight. El Cluster 1 es más heterogéneo y la etiqueta `-1` no se interpreta como un grupo, porque representa perfiles que no alcanzaron la densidad necesaria.

Como controles complementarios, evaluamos PCA y la estabilidad del modelo. PCA produjo grupos muy desbalanceados, por lo que mantuvimos el modelo original. En diez muestras aleatorias del 80 % de los perfiles obtuvimos un ARI promedio de 0,897. Las variables categóricas se utilizaron después del clustering para describir los grupos, no para calcular las distancias.

## 6. Conclusiones generales

El análisis exploratorio nos permitió entender que las fuentes tenían distintos niveles de detalle, que la producción presentaba una distribución sesgada y que existían diferencias importantes según la cuenca, la formación y el tipo de pozo. A partir de esa observación, la regresión fue el enfoque principal: el Random Forest logró un R² de 0,908 y mejoró el MAE y el RMSE respecto del modelo de persistencia, por lo que resultó adecuado para estimar la producción del mes siguiente. La clasificación complementó esa predicción al ordenar los pozos en niveles bajo, medio y alto, con un F1 macro de 0,933 y un desempeño equilibrado entre las clases. Por su parte, DBSCAN permitió reconocer perfiles productivos diferentes: el Cluster 0 concentró los pozos con mayor producción y continuidad, mientras que los Clusters 2 y 3 reunieron principalmente perfiles gasíferos, con baja producción de petróleo y mayor presencia de recursos tight. En conjunto, el proyecto muestra que la historia productiva, las características del pozo y una preparación temporalmente consistente permiten construir predicciones útiles y obtener una visión más completa del comportamiento de los pozos.

## 7. Limitaciones

Los resultados dependen de la calidad y el período disponible de los datos, de las variables seleccionadas y de las decisiones de transformación. Las predicciones para agosto de 2026 no pudieron evaluarse porque el dataset llega hasta julio; además, DBSCAN es sensible a `eps`, `min_samples` y a la representación utilizada, y la construcción de un perfil por pozo resume la historia mensual y pierde parte de su detalle. La etiqueta de ruido no representa un grupo homogéneo, las variables categóricas se utilizaron para describir los clusters y no demuestran causalidad, y el estado y el sistema de extracción corresponden al último registro disponible hasta julio de 2026, no a toda la trayectoria del pozo.

## Resultados y archivos generados

Las notebooks generan datasets procesados, predicciones y resultados de clustering dentro de `data/processed/`. Entre los archivos principales se encuentran los perfiles con clusters, los resúmenes productivos, las grillas de evaluación, el análisis de estabilidad y las predicciones de los modelos supervisados.

Estos archivos se generan al ejecutar las notebooks y no reemplazan a los datasets originales. La documentación completa de cada transformación, métrica, gráfico y decisión se encuentra en las notebooks correspondientes.

## Estructura del repositorio

```text
oil-production-prediction/
├── data/
│   ├── raw/                    # Datos originales, sin modificar
│   └── processed/              # Datos integrados y resultados
├── notebooks/
│   ├── 01_exploracion_datos.ipynb
│   ├── 02_preprocesamiento.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modelado_regresion.ipynb
│   ├── 05_modelado_clasificacion.ipynb
│   ├── 06_exploracion_clustering.ipynb
│   └── 07_modelado_clustering.ipynb
├── reports/                   # Gráficos y material de presentación
├── src/                       # Código reutilizable
├── descargar_datos.py
├── requirements.txt
└── README.md
```

## Instalación y reproducción

### 1. Crear el entorno e instalar las dependencias

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Descargar los datasets

Los archivos originales se encuentran en la carpeta compartida de [Google Drive del proyecto](https://drive.google.com/drive/folders/1l-TYX0l0IWjVZt5Qydmubce5VOd4KvU2). También se pueden obtener desde el ZIP compartido por el equipo.

Hay dos alternativas para incorporarlos al proyecto:

**Opción A: descarga automática**

```powershell
python descargar_datos.py
```

El script descarga los archivos y los guarda automáticamente en `data/raw/`. Para utilizar esta opción, la carpeta de Google Drive debe estar disponible para su lectura.

**Opción B: descarga manual**

1. Descargar el ZIP o los archivos desde Google Drive.
2. Descomprimirlos si es necesario.
3. Copiarlos dentro de `data/raw/`.
4. Verificar que los archivos originales mantengan sus nombres y no sean modificados.

La carpeta `data/raw/` debe contener los archivos originales antes de ejecutar las notebooks. No es necesario subir estos archivos al repositorio, porque son pesados y están excluidos por `.gitignore`.

### 3. Ejecutar las notebooks

Después de disponer de los archivos en `data/raw/`, se deben ejecutar las notebooks en orden numérico, seleccionando `.venv` como kernel:

```text
01_exploracion_datos.ipynb
02_preprocesamiento.ipynb
03_feature_engineering.ipynb
04_modelado_regresion.ipynb
05_modelado_clasificacion.ipynb
06_exploracion_clustering.ipynb
07_modelado_clustering.ipynb
```

La guía completa de cada transformación, modelo, métrica y decisión se encuentra dentro de las notebooks.

## Entrega final y storytelling

El repositorio reúne las fuentes de datos, el análisis exploratorio, la preparación, los modelos supervisados y el modelo no supervisado. Para la presentación oral contamos la historia del proyecto a partir de las preguntas iniciales, los hallazgos del AED, las decisiones de modelado, los resultados obtenidos y las limitaciones.
