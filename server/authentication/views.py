import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout

from userprofile.models import UserProfile, ProfileAvatar
from authentication.serializers import RegistrationSerializer


class SignIn(APIView):
    """
    Эндпоинт для авторизации пользователя.
    """

    def post(self, request: Request) -> Response:
        user_data = json.loads(list(request.POST.keys())[0])
        username = user_data.get("username")
        password = user_data.get("password")

        if username == "" or password == "":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignUpView(APIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """

    def post(self, request):
        data = json.loads(list(request.data.keys())[0])
        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid():
            user = User.objects.create_user(
                password=serializer.validated_data["password"],
                username=serializer.validated_data["username"],
            )
            name = "nameless" if data["name"] is None else data["name"]
            avatar = ProfileAvatar.objects.create(src=None, alt=None)
            UserProfile.objects.create(user=user, fullName=name, avatar=avatar)
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    """
    Эндпоинт для выхода пользователя (Sign Out).
    """

    def post(self, request: Request) -> Response:
        permission_classes = [IsAuthenticated]
        logout(request=request)
        return Response(status=status.HTTP_200_OK)
