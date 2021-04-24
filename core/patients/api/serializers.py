from rest_framework import serializers

from patients.models import Patient, MRI


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "name", "sex", "age", "identity_number", "municipality", "province")


class MRISerializer(serializers.ModelSerializer):
    class Meta:
        model = MRI
        fields = ("id", "datetime", "label", "file", "patient")


class PatientParamSerializer(serializers.Serializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
