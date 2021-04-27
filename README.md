## Segmentación de imagenes DICOM asistida por IA

### Correr servidor django

#### Dependencieas del sistema

- Python 3.9
- PostgreSQL 9.5+
- unrar -> `sudo apt-get install unrar`

Correr esto en `core`:

`poetry install`

Una vez instalado todo:

Crear una base de datos en postgresql llamada `mri-segmentation`

`poetry run ./manage.py migrate`
`poetry run ./manage.py runserver 8000`

Listo!.
