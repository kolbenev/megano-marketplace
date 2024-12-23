from django.urls import path
from userprofile.views import ProfileAPIView, UpdatePasswordView, UpdateAvatarView

urlpatterns = [
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("profile/avatar/", UpdateAvatarView.as_view(), name="update-avatar"),
    path("profile/password/", UpdatePasswordView.as_view(), name="update-password"),
]
