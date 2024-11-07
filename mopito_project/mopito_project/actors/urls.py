from rest_framework.routers import DefaultRouter

from mopito_project.actors.api.views import ClinicViewSet, PatientViewSet, StaffViewSet, SubscriptionViewSet, TimeSlotViewSet


router = DefaultRouter()

app_name = "actors"

router.register("patients", PatientViewSet)
router.register("staffs", StaffViewSet)
router.register("time_slots", TimeSlotViewSet)
router.register("subscriptions", SubscriptionViewSet)
router.register("clinics", ClinicViewSet)

urlpatterns = []
urlpatterns += router.urls
