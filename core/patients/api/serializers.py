from rest_framework import serializers

from patients.models import MRI, Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "name", "sex", "age", "identity_number", "municipality", "province")


class MRISerializer(serializers.ModelSerializer):
    class Meta:
        model = MRI
        fields = ("id", "datetime", "label", "file", "patient", "thumbnail", "segmented_images")

    def create(self, validated_data):
        instance: MRI = super().create(validated_data)
        instance.build_segmented_images()
        return instance


class PatientParamSerializer(serializers.Serializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
