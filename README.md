## Segmentación de imagenes DICOM asistida por IA

## Correr servidor django

## Dependencieas del sistema

- Python 3.9
- PostgreSQL 9.5+
- unrar -> `sudo apt-get install unrar`

Correr esto en `core`:

`poetry install`

## Una vez instalado todo:

### Crear una base de datos en postgresql llamada `mri-segmentation`

#### Crea un archivo con extension `.env` al mismo nivel de `manage.py` con las siguientes varaibles:

```
SECRET_KEY=django-insecure-zp@9n_b^eyqr-omtk3t9(5koe%q#dd)$6)!kjf2+6b7kaej9@f
POSTGRES_DB=mri-segmentation
POSTGRES_USER=postgres
POSTGRES_PASS=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=''
```
### Corre esto para iniciar el servidor

```
poetry run manage.py migrate
poetry run manage.py runserver 8000
```

#### Y si no esta usando un enviroment basado en unix estos

```
poetry run python manage.py migrate
poetry run python manage.py runserver 8000
```

Listo!.
