from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChoiceViewSet,
    LogoutView,
    MeView,
    ScopedTokenObtainPairView,
    ScopedTokenRefreshView,
    SignupView,
    StoryNodeViewSet,
    StoryViewSet,
    UserProgressViewSet,
)

router = DefaultRouter()
router.register(r"stories", StoryViewSet, basename="story")
router.register(r"nodes", StoryNodeViewSet, basename="node")
router.register(r"choices", ChoiceViewSet, basename="choice")
router.register(r"progress", UserProgressViewSet, basename="progress")

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/", ScopedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", ScopedTokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
