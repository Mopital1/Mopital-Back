from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from mopito_project.users.api.views import GroupViewSet, PermissionViewSet, ProfileViewSet, UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("permissions", PermissionViewSet)
router.register("groups", GroupViewSet)
router.register("profile", ProfileViewSet)


app_name = "api"
urlpatterns = router.urls
