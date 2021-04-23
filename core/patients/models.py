from datetime import datetime
from hashlib import md5

from django.db import models
from django.db.models.enums import TextChoices
from django.utils.encoding import smart_bytes
from django.utils.translation import ugettext as _


class Sex(TextChoices):
    Male = "male", _("Masculino")
    Female = "female", _("Femenino")
    Other = "other", _("Otro")


class Patient(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=20, choices=Sex.choices, default=Sex.Other)
    age = models.PositiveIntegerField(null=True, blank=True)
    identity_number = models.CharField(max_length=10, blank=True)
    municipality = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} - {self.identity_number}"


def file_name(instance, filename):
    ext = (filename.split(".")[1:] or ["dicom"]).pop().lower()
    now = datetime.now()
    checksum = md5(smart_bytes(f"{instance.patient.name}{now}")).hexdigest()
    return f"{checksum}.{ext}"


class MRI(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    file = models.FileField(upload_to=file_name)

    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="resonances")
