import shutil

from django.core.management.base import BaseCommand

from patients.models import MRI
from patients.utils import MRIThumbnailsManager


class Command(BaseCommand):
    help = "Re construye las imagenes en png de las imagenes dicom que existen"

    def add_arguments(self, parser):
        parser.add_argument(
            "-mc",
            "--maintain-created",
            action="store_true",
            dest="maintain_created",
            help="No borrar las imagenes ya creadas",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        if not options["maintain_created"]:
            images_path = MRIThumbnailsManager.get_main_folder_path()
            shutil.rmtree(images_path)
            self.stdout.write(f"Se elimino el directorio {images_path}")

        for mri in MRI.objects.all():
            thumbs_manager = MRIThumbnailsManager(mri)
            if options["maintain_created"] and thumbs_manager.get_mri_path().exists():
                self.stdout.write(f"Saltando {str(mri)}")
                self.stdout.write()
            else:
                self.stdout.write(f"Re-construyendo las imagenes de {str(mri)}")
                mri.build_segmented_images()
                self.stdout.write(f"Se termino de construir las imagenes de {str(mri)}")
                self.stdout.write()
