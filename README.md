# Predicción de producción de petróleo en pozos no convencionales

Proyecto final del curso **EnergIA Digital – Data Science** de Fundación YPF.

**Grupo: 6**

**Integrantes:**

- Alex Paredes — DNI 43.790.733
- Julián Varela — DNI XX.XXX.XXX

## Objetivo

El objetivo del proyecto es analizar la producción de petróleo de pozos no convencionales de Argentina y desarrollar modelos de aprendizaje automático para predecir su comportamiento productivo.

La pregunta principal del proyecto es:

> Dadas las características de un pozo y su historial de producción, ¿cuánto petróleo esperamos que produzca el próximo mes?

Para abordar esta problemática se prevé trabajar con tres enfoques:

- **Regresión:** predecir el volumen de producción de petróleo del próximo mes.
- **Clasificación:** categorizar la producción futura en distintos niveles.
- **Clustering:** identificar grupos de pozos con características y comportamientos productivos similares.

## Fuente y contexto de los datos

Los datos utilizados provienen de **Datos Argentina**, el portal oficial de datos abiertos del Gobierno de la República Argentina. Los archivos fueron obtenidos desde la sección relacionada con pozos de petróleo y gas:

[Datos Argentina – Pozos](https://www.datos.gob.ar/datasetproduccion-de-petroleo-y-gas-por-pozo)

La carpeta compartida de Google Drive fue utilizada únicamente como medio de distribución de los archivos entre los integrantes del grupo. La fuente original de la información es el portal oficial de Datos Argentina y los organismos públicos responsables de la información energética.

Los datos representan información de pozos no convencionales de hidrocarburos en Argentina. Incluyen registros de producción de petróleo, gas y agua, características generales de los pozos e información relacionada con operaciones de fracturación y terminación.

Los archivos fueron descargados el **miércoles 16 de septiembre de 2026**. El período temporal analizado comprende desde **noviembre de 2006** hasta **agosto de 2026**, según las fechas disponibles en los archivos.

## Datasets utilizados

El proyecto utiliza los siguientes archivos:

- `produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv`: contiene registros de producción mensual de petróleo, gas, agua y otros indicadores productivos por pozo.
- `capitulo-iv-pozos.csv`: contiene características generales de los pozos, como ubicación, profundidad, formación, cuenca, tipo de recurso y tipo de extracción.
- `datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv`: contiene información relacionada con las operaciones de fracturación y terminación de los pozos.

Los datasets tienen diferentes niveles de detalle. La información de producción se encuentra principalmente a nivel pozo-mes, mientras que las características generales corresponden al nivel pozo. Los datos de fracturación pueden contener más de un registro por pozo, debido a la existencia de distintas operaciones o etapas.

El identificador utilizado para relacionar las fuentes es `idpozo`, aunque antes de realizar los cruces se debe verificar la unicidad y la granularidad de cada archivo.

## Análisis exploratorio

Durante el análisis exploratorio se realizaron las siguientes tareas:

- Lectura e inspección inicial de los archivos.
- Análisis de dimensiones, columnas y tipos de datos.
- Identificación de valores faltantes y registros duplicados.
- Revisión de la granularidad de cada dataset.
- Análisis de las fechas y del período cubierto.
- Estudio de variables numéricas y categóricas.
- Detección de valores inconsistentes o potencialmente inválidos.
- Análisis de la distribución de la producción.
- Visualización de la producción por año, pozo, formación, cuenca y tipo de recurso.
- Exploración de la relación entre producción, características de los pozos y fracturación.

Entre los principales aspectos detectados se encuentran la distribución sesgada de la producción, la presencia de valores extremos, registros con valores negativos o nulos en algunas variables y posibles inconsistencias en fechas, profundidades y coordenadas. Estos casos serán revisados antes de construir los modelos.

También se observó que algunas variables pueden estar relacionadas directamente con la producción o haber sido registradas posteriormente al momento de producción. Por este motivo, antes del modelado se analizará la posibilidad de filtrarlas para evitar problemas de fuga de información.

## Variables principales

Entre las variables consideradas se encuentran:

- `idpozo`: identificador del pozo.
- `fecha`: fecha o período correspondiente al registro de producción.
- `prod_pet`: producción de petróleo.
- `prod_gas`: producción de gas.
- `prod_agua`: producción de agua, cuando se encuentra disponible.
- `tef`: variable categórica asociada al tipo o estado del pozo, según la definición del dataset.
- Variables de ubicación, formación, cuenca y profundidad.
- Variables relacionadas con la fracturación y terminación de los pozos.

Las unidades y definiciones específicas de cada variable se revisan en la notebook de análisis exploratorio a partir de la documentación disponible para cada dataset.

## Estructura del repositorio

```text
oil-production-prediction/
│
├── data/
│   ├── raw/                  # Archivos originales, sin modificar
│   └── processed/            # Datos transformados para el análisis o los modelos
│
├── notebooks/
│   └── 01_exploracion_datos.ipynb
│
├── src/                      # Código reutilizable del proyecto
├── reports/                  # Gráficos, resultados y material de presentación
│
├── descargar_datos.py        # Descarga alternativa de los datasets
├── requirements.txt          # Dependencias del proyecto
├── .gitignore
└── README.md
```

Los archivos originales no se incluyen en el repositorio debido a su tamaño. Deben descargarse y ubicarse dentro de `data/raw/`.

## Instalación y uso

Se recomienda utilizar Python 3.11 o una versión compatible.

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Si los archivos no se encuentran disponibles localmente, pueden descargarse desde la carpeta compartida ejecutando:

```bash
python descargar_datos.py
```

El script guarda los archivos dentro de `data/raw/` y omite aquellos que ya existen.

Para ejecutar la notebook desde Visual Studio Code, se debe seleccionar el entorno `.venv` como kernel.

## Próximas etapas

Luego del análisis exploratorio se prevé:

1. Definir los criterios de limpieza y tratamiento de valores inconsistentes.
2. Integrar las distintas fuentes mediante `idpozo`.
3. Crear variables derivadas para representar el historial productivo.
4. Definir la variable objetivo y el período de predicción.
5. Entrenar y evaluar modelos de regresión y clasificación.
6. Aplicar un algoritmo de clustering.
7. Comparar los resultados y seleccionar los enfoques más adecuados.
8. Presentar las conclusiones mediante una propuesta de storytelling.

## Estado del proyecto

Actualmente se encuentran preparados:

- El repositorio y su estructura inicial.
- El entorno virtual y las dependencias.
- Los scripts para descargar los datos.
- La notebook de análisis exploratorio.
- La descripción inicial del problema y de las fuentes de datos.

Las decisiones definitivas de limpieza, integración y modelado se tomarán en las siguientes etapas del proyecto, a partir de los resultados obtenidos durante el análisis exploratorio.
