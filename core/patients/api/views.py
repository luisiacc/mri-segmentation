from rest_framework import viewsets

from patients import models

from .serializers import PatientParamSerializer, PatientSerializer, MRISerializer, DetailMRISerializer


class NestedPatientMixin:
    lookup = "patient"

    def get_patient_pk(self):
        params_serializer = PatientParamSerializer(data=self.request.query_params)
        params_serializer.is_valid(raise_exception=True)
        return params_serializer[self.lookup].value

    def get_patient(self):
        return models.Patient.objects.get(id=self.get_patient_pk())


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = models.Patient.objects.all()


class MRIViewSet(viewsets.ModelViewSet, NestedPatientMixin):
    serializer_class = MRISerializer
    detail_serializer_class = DetailMRISerializer
    queryset = models.MRI.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        else:
            return self.serializer_class

    def get_queryset(self):
        return super().get_queryset().filter(patient__pk=self.get_patient_pk())
