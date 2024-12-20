from rest_framework.routers import DefaultRouter

from mopito_project.appointments.api.views import AppointmentViewSet, ConsultationViewSet, ReviewViewSet, AdvertiseViewSet

router = DefaultRouter()

app_name = "appointments"

router.register("appointments", AppointmentViewSet)
router.register("reviews", ReviewViewSet)
router.register("consultations", ConsultationViewSet)
router.register("advertises", AdvertiseViewSet)

urlpatterns = []

urlpatterns += router.urls