# Predicción de Producción de Petróleo en Pozos No Convencionales

Proyecto final del curso **EnergIA Digital – Data Science** de Fundación YPF.

## Objetivo

Analizar la producción de petróleo de pozos no convencionales de Argentina y desarrollar modelos de Machine Learning para predecir su comportamiento productivo.

La pregunta principal que buscamos responder es:

> **Dadas las características de un pozo y su historial de producción, ¿cuánto petróleo esperamos que produzca el próximo mes?**

A partir de esta pregunta se trabajará en tres enfoques:

- **Regresión:** predecir la producción de petróleo del próximo mes.
- **Clasificación:** categorizar la producción futura en niveles de producción.
- **Clustering:** identificar perfiles o grupos de pozos con características y comportamientos similares.

## Datos

Actualmente contamos con tres fuentes principales:

- `produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv`: producción mensual de petróleo, gas, agua y otros indicadores de pozos no convencionales.
- `capitulo-iv-pozos.csv`: características generales de los pozos, como profundidad, formación, cuenca, tipo de recurso y tipo de extracción.
- `datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv`: información relacionada con la fracturación y terminación de los pozos.

Los archivos originales no se incluyen en el repositorio debido a su tamaño. Cada integrante debe obtenerlos desde el ZIP compartido por el equipo y colocarlos en:

```text
data/raw/
├── produccin-de-pozos-de-gas-y-petrleo-no-convencional.csv
├── capitulo-iv-pozos.csv
└── datos-de-fractura-de-pozos-de-hidrocarburos-adjunto-iv-actualizacin-diaria.csv
```

Si el ZIP no está disponible, los archivos se pueden descargar desde la [carpeta compartida de Google Drive](https://drive.google.com/drive/folders/1l-TYX0l0IWjVZt5Qydmubce5VOd4KvU2?usp=sharing) ejecutando:

```bash
python descargar_datos.py
```

El script guarda los archivos en `data/raw/` y omite los que ya existen. Requiere el entorno virtual activo con las dependencias instaladas (ver [Entorno de trabajo](#entorno-de-trabajo)).

Los archivos de `data/raw/` se mantienen sin modificar.

## Estructura del proyecto

```text
oil-production-prediction/
│
├── data/
│   ├── raw/          # Datos originales
│   └── processed/    # Datos transformados y preparados para los modelos
│
├── notebooks/        # Análisis exploratorio y modelos
├── src/              # Código reutilizable
├── reports/          # Gráficos, resultados y material de presentación
│
├── descargar_datos.py  # Descarga alternativa de los datos desde Google Drive
├── .gitignore
├── requirements.txt
└── README.md
```

## Entorno de trabajo

El proyecto utiliza un entorno virtual de Python para mantener las mismas dependencias entre los integrantes.

Se requiere **Python 3.11 o superior** (algunas dependencias, como `pandas` 3 y `numpy` 2.5, no funcionan con versiones anteriores).

Crear el entorno:

```bash
python -m venv .venv
```

En macOS, el `python3` del sistema suele ser 3.9. Si usás pyenv, fijá primero una versión compatible con `pyenv local 3.12.7`.

Activarlo en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activarlo en macOS / Linux:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Para usar el entorno en los notebooks de VS Code, seleccionar `.venv` como kernel con el botón **Select Kernel**.
Las versiones de las principales librerías utilizadas se encuentran registradas en `requirements.txt`.

## Flujo de trabajo previsto

El proyecto se desarrollará en distintas etapas:

1. Exploración y análisis de los datos (EDA/AED).
2. Limpieza y preparación de los datos.
3. Integración de las diferentes fuentes mediante `idpozo`.
4. Ingeniería de características.
5. Desarrollo de modelos de regresión.
6. Desarrollo de modelos de clasificación.
7. Evaluación y ajuste de los modelos.
8. Desarrollo de modelos de clustering.
9. Análisis de resultados.
10. Storytelling y presentación final.

## Trabajo colaborativo

El repositorio de GitHub contiene el código, notebooks, documentación y configuración del proyecto.

Los datos originales y el entorno virtual `.venv` se mantienen localmente y no se suben al repositorio.

Flujo básico de Git:

```text
Modificar archivos
      ↓
git add
      ↓
git commit
      ↓
git push
      ↓
GitHub
```

Para obtener los cambios realizados por otro integrante:

```bash
git pull
```

## Estado actual

Actualmente se encuentra preparado:

- Repositorio de GitHub.
- Estructura inicial de carpetas.
- Entorno virtual de Python.
- Dependencias registradas en `requirements.txt`.
- Datos originales ubicados localmente en `data/raw/`.
- `.gitignore` configurado para evitar subir los datasets.

### Próximos pasos

- Confirmar y documentar las fuentes originales de los datos.
- Realizar el análisis exploratorio.
- Verificar calidad, duplicados y valores faltantes.
- Analizar la relación entre producción, características de los pozos y fracturación.
- Definir las variables finales para los modelos.
