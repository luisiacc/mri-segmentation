from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import ugettext as _

import rarfile

from dicom_processing.utils import Cut, dicom2png

from .utils import MRIDecompressManager, MRIThumbnailsManager, get_file_url

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
        return f"MRI for {self.patient.name} - {self.datetime}"

    @property
    def date(self):
        return self.datetime.date()

    @property
    def thumbnail(self):
        builder = MRIThumbnailsManager(self)
        if not builder.get_mri_path().exists():
            return ""
        return builder.get_grouped_images_from_storage()[Cut.Axial][0]

    @property
    def segmented_images(self):
        builder = MRIThumbnailsManager(self)
        return builder.get_grouped_images_from_storage()

    def build_segmented_images(self):
        decompresser = MRIDecompressManager(self)
        builder = MRIThumbnailsManager(self, decompresser)
        if builder.get_mri_path().exists():
            return builder.get_grouped_images_from_storage()
        return builder.build_grouped_images()
