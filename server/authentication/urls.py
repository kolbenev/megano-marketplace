from django.urls import path

from authentication.views import (
    SignIn,
    SignUpView,
    SignOutView,
)

urlpatterns = [
    path("sign-in/", SignIn.as_view(), name="signin"),
    path("sign-up/", SignUpView.as_view(), name="signup"),
    path("sign-out/", SignOutView.as_view(), name="signout"),
]
