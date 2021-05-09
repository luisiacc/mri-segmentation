from datetime import datetime
from pathlib import Path
from typing import Iterable

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import ugettext as _

import rarfile
from dicom_processing.utils import Cut, FileLike, dicom2png, filter_by_series, get_dcm_files_from_rarfile, get_slice_cut

from .utils import MRIThumbnailBuilder, build_mri_segmented_thumbnail

file_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)


class Patient(models.Model):
    class Sex(TextChoices):
        Male = "male", _("Masculino")
        Female = "female", _("Femenino")
        Other = "other", _("Otro")

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=20, choices=Sex.choices, default=Sex.Other)
    age = models.PositiveIntegerField(null=True, blank=True)
    identity_number = models.CharField(max_length=11, blank=True)
    municipality = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} - {self.identity_number}"


def file_name(instance, filename):
    ext = filename.split(".")[-1] if "." in filename else ""
    now = datetime.now().timestamp()
    filename_without_extension = "".join(x for x in filename.split(".")[:-1])
    return f"{filename_without_extension}-{now}.{ext}"


class MRI(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    datetime = models.DateTimeField(null=True, blank=True)

    label = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to=file_name, storage=file_storage)

    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="resonances")

    def __str__(self):
        return f"{self.patient.name} - {self.datetime}"

    @property
    def date(self):
        return self.datetime.date()

    @property
    def thumbnail(self):
        mri_path = Path(self.file.path)
        thumbnail_name = f"{mri_path.name}.png"
        thumbnail_path = Path(f"{settings.PRIVATE_STORAGE_ROOT}/{thumbnail_name}")
        thumbnail_url = f"/{thumbnail_name}"

        if not mri_path.exists() or mri_path.suffix.lower() != ".rar":
            return ""

        if not thumbnail_path.exists():
            rar = rarfile.RarFile(mri_path)
            dcm_list = [x.filename for x in rar.infolist() if x.filename.lower().endswith("dcm")]
            dicom2png(rar.open(dcm_list[0]), str(thumbnail_path))  # noqa

        return thumbnail_url

    def categorized_images(self):
        builder = MRIThumbnailBuilder(self)

        if builder.get_mri_path().exists():
            return builder.get_grouped_images_from_storage()

        return builder.construct_grouped_images()
