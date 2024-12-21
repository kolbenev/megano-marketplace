from django.urls import path
from userprofile.views import ProfileGetAPIView, ProfilePostAPIView, UpdatePasswordView, UpdateAvatarView

urlpatterns = [
    path("profile/", ProfileGetAPIView.as_view(), name="get-profile"),
    path("profile/", ProfilePostAPIView.as_view(), name="post-profile"),
    path("profile/avatar/", UpdateAvatarView.as_view(), name="update-avatar"),
    path("profile/password/", UpdatePasswordView.as_view(), name="update-password"),
]
