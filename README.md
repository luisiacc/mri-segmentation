## Segmentación de imagenes DICOM asistida por IA

### Correr servidor django

#### Requerimientos

- Poetry
- Python 3.9
- PostgreSQL 9.5+

Correr esto en `core`:

`poetry install`

Una vez instalado todo:

Crear una base de datos en postgresql llamada `mri-segmentation`

`poetry run ./manage.py migrate`
`poetry run ./manage.py runserver 8000`

Listo!.
