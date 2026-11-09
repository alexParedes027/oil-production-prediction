# Predicción de producción de petróleo en pozos no convencionales

Proyecto final del curso **EnergIA Digital – Data Science** de Fundación YPF.

**Grupo:** 6

**Integrantes:**

- Alex Paredes
- Julián Varela

---

## Tema y objetivo

El proyecto analiza la producción de petróleo de pozos no convencionales de Argentina y aplica técnicas de análisis exploratorio, aprendizaje supervisado y aprendizaje no supervisado.

La pregunta principal que buscamos responder es:

> **Dadas las características de un pozo y su historial de producción, ¿cuánto petróleo esperamos que produzca durante el próximo mes?**

Para responderla trabajamos con tres enfoques:

- **Regresión:** estimar la producción de petróleo del mes siguiente en metros cúbicos.
- **Clasificación:** categorizar la producción futura en niveles bajo, medio y alto.
- **Clustering:** identificar perfiles de pozos con características productivas y operativas similares.

La regresión es el enfoque principal porque responde directamente a la pregunta sobre la cantidad esperada de producción. La clasificación y el clustering complementan el análisis con una interpretación más general de los resultados.

## Fuentes de datos

Los datos fueron obtenidos del portal oficial de datos abiertos de la República Argentina, [Datos Argentina](https://www.datos.gob.ar/datasetproduccion-de-petroleo-y-gas-por-pozo).

Se utilizaron principalmente las siguientes fuentes:

- `produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv`: registros mensuales de producción de petróleo, gas, agua y otros indicadores por pozo.
- `capitulo-iv-pozos.csv`: características generales de los pozos, como profundidad, formación, cuenca, provincia, tipo de pozo y tipo de extracción.
- `datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv`: información relacionada con la fracturación y terminación de los pozos.

También se utilizaron archivos complementarios del mismo conjunto de datos para validar fechas de primera producción y obtener información histórica por cuenca y subtipo de recurso.

El identificador utilizado para integrar las distintas fuentes es `idpozo`.

Los archivos originales son pesados y se mantienen fuera del control de versiones. Se descargan mediante `descargar_datos.py` o se copian desde el ZIP compartido por el equipo dentro de `data/raw/`. La carpeta `data/raw/` conserva los archivos originales sin modificar.

## Estructura del repositorio

```text
oil-production-prediction/
|
|-- data/
|   |-- raw/                              # Datos originales, sin modificar
|   |-- processed/                        # Datos integrados y resultados
|       |-- clustering/                   # Resultados del análisis no supervisado
|
|-- notebooks/
|   |-- 01_exploracion_datos.ipynb
|   |-- 02_preprocesamiento.ipynb
|   |-- 03_feature_engineering.ipynb
|   |-- 04_modelado_regresion.ipynb
|   |-- 05_modelado_clasificacion.ipynb
|   |-- 06_exploracion_clustering.ipynb
|   |-- 07_modelado_clustering.ipynb
|
|-- reports/                              # Gráficos y material de presentación
|-- src/                                  # Código reutilizable
|-- descargar_datos.py
|-- requirements.txt
|-- .gitignore
|-- README.md
|-- README2.md
```

## Flujo general de trabajo

El proyecto se desarrolló en las siguientes etapas:

1. Exploración de las fuentes y comprensión de la estructura de los datos.
2. Limpieza, validación e integración mediante `idpozo`.
3. Construcción de una tabla mensual integrada por pozo.
4. Ingeniería de variables históricas y temporales.
5. Definición del objetivo de producción del mes siguiente.
6. Entrenamiento y evaluación de modelos de regresión y clasificación.
7. Construcción de perfiles agregados, uno por pozo, para clustering.
8. Aplicación, evaluación y validación de DBSCAN.
9. Interpretación de los perfiles con variables productivas, físicas y categóricas.
10. Preparación de resultados para el storytelling y la presentación final.

## 1. Análisis exploratorio de datos

En `01_exploracion_datos.ipynb` analizamos las fuentes originales con Pandas y visualizaciones estadísticas.

Se revisaron:

- Cantidad de filas y columnas.
- Nombres y tipos de variables.
- Valores faltantes.
- Duplicados e identificadores.
- Granularidad y período temporal.
- Distribución de la producción.
- Tipos de pozos.
- Cuencas, provincias y formaciones.
- Diferencias entre las fuentes.
- Valores extremos e inconsistencias.
- Relación entre producción y características de los pozos.

El análisis mostró que las fuentes tenían distintos niveles de detalle y que la producción presentaba una distribución sesgada, con diferencias importantes entre pozos. Estos resultados guiaron las decisiones de limpieza, integración y transformación posteriores.

## 2. Preprocesamiento e integración

En `02_preprocesamiento.ipynb` se validaron y limpiaron las fuentes antes de integrarlas.

Las principales tareas fueron:

- Normalización de fechas y nombres de variables.
- Revisión de unidades.
- Validación de claves e identificadores.
- Tratamiento de duplicados.
- Integración mediante `idpozo`.
- Incorporación de información de pozos y fracturación.
- Construcción de una tabla mensual integrada.
- Validación de la integridad temporal.
- Creación de la variable objetivo de regresión.

La unidad de análisis para los modelos supervisados quedó definida como un registro de un pozo en un determinado mes.

## 3. Ingeniería de variables y partición temporal

En `03_feature_engineering.ipynb` se construyeron variables utilizando únicamente la información disponible hasta cada mes de corte.

Se generaron, entre otras:

- Producción del mes de corte.
- Rezagos de producción.
- Medias móviles.
- Desvíos y cambios recientes.
- Producción acumulada.
- Producción por día.
- Meses desde el inicio.
- Características operativas y geológicas.
- Información de fracturación.
- Variables categóricas del pozo.

El objetivo de regresión fue:

```text
prod_pet_mes_siguiente
```

Esta variable representa la producción de petróleo del mismo pozo durante el mes siguiente al mes de corte.

Para evitar utilizar información futura, se utilizaron particiones temporales:

- **Entrenamiento:** objetivos desde enero de 2020 hasta diciembre de 2025.
- **Validación:** objetivos de enero a marzo de 2026.
- **Test:** objetivos de abril a julio de 2026.
- **Inferencia:** información disponible hasta julio de 2026 para estimar agosto de 2026.

También se compararon ventanas de entrenamiento más cortas y más extensas. La ventana desde 2020 presentó una mejora moderada y consistente, por lo que fue seleccionada para el modelo final.

## 4. Modelo de regresión

En `04_modelado_regresion.ipynb` se desarrolló el modelo principal del proyecto.

Se compararon:

- Modelo de persistencia.
- Random Forest Regressor.
- Ridge.
- Estrategia de dos etapas basada en clasificación y regresión.

El modelo de persistencia se utilizó como referencia y supone que la producción del próximo mes será igual a la producción del mes de corte.

El modelo final seleccionado fue un **Random Forest Regressor**. En el conjunto de test se obtuvieron los siguientes resultados:

| Modelo              | MAE (m³) | RMSE (m³) |    R² |
| ------------------- | -------: | --------: | ----: |
| Persistencia        |  166,195 |   551,710 | 0,820 |
| Random Forest final |  133,039 |   393,443 | 0,908 |

Respecto de la persistencia, el modelo final:

- Redujo aproximadamente un 20 % el MAE.
- Redujo aproximadamente un 29 % el RMSE.
- Obtuvo un R² de 0,908.
- No generó predicciones negativas.

El modelo fue utilizado para estimar la producción de agosto de 2026 a partir de la información disponible hasta julio. Se generaron predicciones para 5.062 pozos. Como la producción real de agosto todavía no está disponible, esas predicciones no tienen una evaluación posterior.

## 5. Modelo de clasificación

En `05_modelado_clasificacion.ipynb` se desarrolló un modelo complementario para categorizar la producción futura.

La variable objetivo fue:

```text
clase_prod_pet_mes_siguiente
```

Las categorías utilizadas fueron:

- `Baja`.
- `Media`.
- `Alta`.

Se comparó el modelo con una referencia que siempre predice la clase mayoritaria. El clasificador seleccionado fue un **Random Forest Classifier**, con `max_features=0,7`.

En el conjunto de test obtuvo:

| Métrica           | Resultado |
| ----------------- | --------: |
| Accuracy          |     0,935 |
| Balanced accuracy |     0,932 |
| Precision macro   |     0,933 |
| Recall macro      |     0,932 |
| F1 macro          |     0,933 |

El modelo presentó un desempeño equilibrado entre las tres clases. La categoría `Media` fue la más difícil de distinguir, porque se encuentra entre los niveles bajo y alto.

También se generaron categorías estimadas para agosto de 2026. Estas predicciones no pueden evaluarse todavía porque aún no se conoce la producción real de ese mes.

## 6. Exploración para clustering

En `06_exploracion_clustering.ipynb` se cambió la unidad de análisis. Mientras que los modelos supervisados trabajan con registros mensuales, el clustering utiliza una fila por pozo.

El dataset integrado contiene:

- 421.046 registros mensuales.
- 5.089 pozos.
- Período desde enero de 2006 hasta julio de 2026.

Se conservaron los pozos con al menos seis meses observados. Como resultado se obtuvieron:

- 4.839 pozos.
- Una fila por pozo.
- 29 columnas con información productiva, temporal, física, geológica y categórica.

Para cada pozo se construyeron perfiles con variables como:

- Producción media, mediana, máxima y acumulada.
- Desvío de producción.
- Meses observados y meses productivos.
- Porcentaje de meses productivos.
- Producción del último mes.
- Promedios móviles de 3 y 6 meses.
- Cambio reciente.
- Meses desde el inicio.
- Profundidad, cota y `tef`.
- Estado, extracción, tipo de pozo, empresa, cuenca, provincia, formación y recurso.

Las variables categóricas no se utilizaron para formar los grupos. Se conservaron para interpretar los clusters después del modelado.

## 7. Modelo de clustering con DBSCAN

En `07_modelado_clustering.ipynb` se aplicó DBSCAN sobre 16 variables numéricas.

Antes del modelado:

- Se excluyeron identificadores, fechas y variables categóricas.
- Se aplicó `log1p` a variables productivas y de cantidad de meses.
- Se mantuvieron sin logaritmo las variables con valores negativos o con una interpretación diferente.
- Se utilizó `StandardScaler` para llevar las variables a una escala comparable.

DBSCAN fue elegido porque:

- No exige definir previamente la cantidad de grupos.
- Trabaja con zonas de distinta densidad.
- Permite detectar observaciones que no pertenecen claramente a ningún grupo.
- Identifica esas observaciones con la etiqueta `-1`.

Se evaluaron distintas combinaciones de `eps` y `min_samples` mediante una grilla. Para comparar las configuraciones se utilizaron:

- Cantidad de grupos.
- Porcentaje de ruido.
- Porcentaje de pozos asignados.
- Tamaño del grupo mayor y menor.
- Silhouette.
- Calinski-Harabasz.
- Davies-Bouldin.

La configuración seleccionada fue:

```text
eps = 1,2
min_samples = 24
```

El modelo produjo:

- 4 grupos.
- 3.979 pozos asignados.
- 860 pozos considerados ruido.
- 82,23 % de pozos asignados.
- 17,77 % de ruido.

La configuración con mayor silhouette no fue seleccionada automáticamente porque dejaba fuera una proporción excesiva de pozos. También se descartaron configuraciones que concentraban más del 98 % de los pozos en un único grupo.

## 8. Interpretación de los clusters

Los perfiles productivos principales fueron:

### Cluster 0

Es el grupo más numeroso, con 3.082 pozos. Presenta la mayor producción media, alta continuidad productiva y una proporción elevada de meses productivos. Está compuesto principalmente por pozos petrolíferos, asociados con Vaca Muerta y recursos shale.

### Cluster 1

Está compuesto por 336 pozos. Presenta una producción media mucho menor que el Cluster 0, menor continuidad y producción reciente casi nula. Su composición es más heterogénea y contiene una proporción importante de pozos clasificados como `Otro tipo`.

### Cluster 2

Está compuesto por 328 pozos. Presenta producción de petróleo prácticamente nula y una proporción muy baja de meses productivos. Está formado principalmente por pozos gasíferos y tiene una mayor proporción de recursos tight, con presencia destacada de la formación Lajas.

### Cluster 3

Está compuesto por 233 pozos. También presenta producción petrolera prácticamente nula y muy pocos meses productivos. Está formado principalmente por pozos gasíferos y recursos tight, con mayor presencia relativa de Vaca Muerta.

### Ruido

Los 860 pozos etiquetados como `-1` no forman un grupo homogéneo. Son perfiles que no alcanzaron la densidad necesaria para integrarse a un cluster y presentan características diversas. Por este motivo, se los utiliza como referencia, pero no se les asigna un perfil único.

## 9. PCA y comparación de representaciones

Se aplicó PCA como herramienta complementaria para estudiar la estructura de los datos y facilitar la visualización.

Las primeras siete componentes explicaron aproximadamente el 97 % de la variabilidad. Sin embargo, al aplicar DBSCAN sobre esas siete componentes, las mejores configuraciones produjeron solamente dos grupos, con más del 98 % de los pozos concentrados en un único grupo.

Por este motivo, PCA no fue utilizada como representación principal del clustering. Se mantuvo el modelo original de DBSCAN sobre las 16 variables transformadas y escaladas.

## 10. Estabilidad del modelo

La estabilidad se evaluó aplicando nuevamente DBSCAN sobre diez muestras aleatorias del 80 % de los perfiles.

Los resultados fueron:

- Entre 5 y 6 grupos en las muestras.
- Porcentaje medio de ruido de 22,14 %.
- ARI medio respecto del modelo completo de 0,897.
- Desvío estándar del ARI de 0,017.

El ARI cercano a 1 indica que las asignaciones generales se mantuvieron similares. La diferencia en la cantidad de grupos y el aumento del ruido son esperables porque al trabajar con menos observaciones cambia la densidad local.

Estos resultados respaldan que la estructura principal encontrada por DBSCAN es estable.

## 11. Interpretación mediante variables categóricas

Luego de obtener los grupos, se analizaron variables categóricas que no participaron en el cálculo de las distancias:

- Cuenca.
- Provincia.
- Formación.
- Tipo de pozo.
- Tipo de extracción.
- Estado.
- Subtipo de recurso.

Los principales hallazgos fueron:

- La cuenca Neuquina predomina en todos los grupos.
- Vaca Muerta es la formación más frecuente, aunque Lajas tiene mayor presencia relativa en el Cluster 2.
- El Cluster 0 presenta predominio de pozos petrolíferos.
- Los Clusters 2 y 3 están compuestos principalmente por pozos gasíferos.
- Los Clusters 2 y 3 presentan una mayor proporción de recursos tight.
- El estado más reciente y el sistema de extracción ayudan a describir los grupos, pero no explican por sí solos todo el comportamiento productivo.

Para las variables categóricas que cambian a lo largo del tiempo se conservó el último valor disponible por pozo, hasta julio de 2026. Por lo tanto, el estado y el sistema de extracción representan la situación más reciente registrada y no todo el historial del pozo.

Las asociaciones observadas son descriptivas y no deben interpretarse como relaciones causales.

## 12. Limitaciones

Los resultados deben interpretarse considerando las siguientes limitaciones:

- DBSCAN depende de la selección de `eps` y `min_samples`.
- La inclusión o exclusión de variables puede modificar las distancias y los grupos.
- Las variables productivas fueron resumidas en una fila por pozo, por lo que no se conserva todo el detalle mensual.
- La etiqueta `-1` representa ruido y no un grupo homogéneo.
- Las variables categóricas se utilizaron después del clustering y no formaron parte del modelo.
- El estado y el sistema de extracción representan el último registro disponible, no toda la historia.
- Las métricas internas ayudan a comparar configuraciones, pero no determinan por sí solas cuál es el agrupamiento correcto.
- La estabilidad se evaluó mediante muestras del 80 % de los perfiles y no elimina completamente la sensibilidad de DBSCAN.
- Los clusters deben interpretarse como perfiles descriptivos, no como categorías definitivas ni como relaciones causales.

## Archivos de resultados

La notebook de clustering exporta los resultados en:

```text
data/processed/clustering/
|-- estabilidad_dbscan.csv
|-- grilla_dbscan.csv
|-- grilla_dbscan_pca.csv
|-- perfiles_con_clusters.csv
|-- resumen_perfiles.csv
|-- resumen_productivo_clusters.csv
```

También se generan en `data/processed/` los datasets utilizados por los modelos supervisados y las predicciones correspondientes a agosto de 2026.

## Instalación y reproducción

Se recomienda utilizar Python 3.11 o una versión compatible.

### Crear el entorno virtual

```bash
python -m venv .venv
```

### Activarlo en Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Instalar las dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Descargar los datos

Si los archivos no se encuentran en `data/raw/`, se puede ejecutar:

```powershell
python descargar_datos.py
```

Luego se deben ejecutar las notebooks en este orden:

```text
01_exploracion_datos.ipynb
02_preprocesamiento.ipynb
03_feature_engineering.ipynb
04_modelado_regresion.ipynb
05_modelado_clasificacion.ipynb
06_exploracion_clustering.ipynb
07_modelado_clustering.ipynb
```

Las notebooks deben ejecutarse seleccionando el entorno `.venv` como kernel de Python. Las rutas están preparadas para ejecutarse desde el directorio `notebooks/`.

## Entrega final

El repositorio contiene:

- Análisis exploratorio.
- Preprocesamiento e integración.
- Ingeniería de variables.
- Modelo supervisado de regresión.
- Modelo supervisado de clasificación.
- Modelo no supervisado de clustering.
- Evaluación, comparación y limitaciones.
- Resultados exportados.
- Documentación del flujo completo.
