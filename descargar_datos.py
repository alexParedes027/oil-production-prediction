"""Descarga los datasets del proyecto desde la carpeta compartida de Google Drive.

Alternativa al ZIP compartido por el equipo: usarlo solo si el ZIP no está
disponible. Los archivos se guardan en `data/raw/`, igual que los del ZIP.

Uso:
    python descargar_datos.py
"""

import sys
from pathlib import Path

try:
    import gdown
except ImportError:
    sys.exit("Falta la librería gdown. Instalala con: pip install gdown")

DRIVE_FOLDER_URL = (
    "https://drive.google.com/drive/folders/1l-TYX0l0IWjVZt5Qydmubce5VOd4KvU2"
)
DATASETS_DIR = Path(__file__).resolve().parent / "data" / "raw"


def main():
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Descargando archivos en: {DATASETS_DIR}")

    # skip_download=True solo lista los archivos, así se omiten los ya descargados
    archivos = gdown.download_folder(
        url=DRIVE_FOLDER_URL, output=str(DATASETS_DIR), skip_download=True, quiet=True
    )
    if not archivos:
        sys.exit("No se encontraron archivos. Verificá que la carpeta sea pública.")

    for archivo in archivos:
        destino = Path(archivo.local_path)
        if destino.exists():
            print(f"Ya existe, se omite: {destino.name}")
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        gdown.download(id=archivo.id, output=str(destino), quiet=False)

    print("Descarga finalizada.")


if __name__ == "__main__":
    main()
