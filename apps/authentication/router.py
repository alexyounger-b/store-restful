from django.urls.conf import path
from rest_framework import routers

from apps.authentication.views import AuthenticationViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register("authentication", AuthenticationViewSet, basename="authentication")

urlpatterns = [
    path(
        "profile/",
        ProfileViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update"}),
        name="profile",
    )
] + router.urls
