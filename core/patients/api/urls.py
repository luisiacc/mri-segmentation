from rest_framework.routers import DefaultRouter

from .views import MRIViewSet, PatientViewSet

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("mris", MRIViewSet, basename="mri")

urlpatterns = router.urls
