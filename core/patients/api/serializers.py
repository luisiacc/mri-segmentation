from rest_framework import serializers

from patients.models import Patient, MRI


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "name", "sex", "age", "identity_number", "municipality", "province")


class MRISerializer(serializers.ModelSerializer):
    class Meta:
        model = MRI
        fields = ("id", "datetime", "label", "file", "patient", "thumbnail")


class DetailMRISerializer(MRISerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = MRI
        fields = MRISerializer.Meta.fields + ("images",)

    def get_images(self, obj):
        return obj.categorized_images()


class PatientParamSerializer(serializers.Serializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
