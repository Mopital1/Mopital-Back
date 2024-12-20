from rest_framework.routers import DefaultRouter

from mopito_project.actors.api.views import (
    ClinicViewSet, 
    CountryViewSet, 
    PatientViewSet, 
    ProfileViewSet, 
    SpecialityViewSet, 
    StaffViewSet, 
    SubscriptionViewSet, 
    TimeSlotViewSet,
    DocumentViewSet,
    MedicalFolderViewSet,
    PricingViewSet,
    PaymentMethodViewSet,
    StaffPathViewSet
)


router = DefaultRouter()

app_name = "actors"

router.register("patients", PatientViewSet)
router.register("staffs", StaffViewSet)
router.register("time_slots", TimeSlotViewSet)
router.register("subscriptions", SubscriptionViewSet)
router.register("clinics", ClinicViewSet)
router.register("profile", ProfileViewSet)
router.register("countries", CountryViewSet)
router.register("specialities", SpecialityViewSet),
router.register("medical_folders", MedicalFolderViewSet),
router.register("documents", DocumentViewSet),
router.register("staff_paths", StaffPathViewSet),
router.register("payment_methods", PaymentMethodViewSet),
router.register("pricings", PricingViewSet)



urlpatterns = []
urlpatterns += router.urls
