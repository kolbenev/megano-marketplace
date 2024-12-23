from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from userprofile.models import UserProfile, ProfileAvatar
from userprofile.serializers import ProfileUserSerializer


class ProfileAPIView(APIView):
    def get(self, request: Request) -> Response:
        """
        Вывод информации о пользователе.
        """
        permission_classes = [IsAuthenticated]
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = ProfileUserSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Обновление информации и пользователе.
        """
        permission_classes = [IsAuthenticated]
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = ProfileUserSerializer(
            user_profile, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAvatarView(APIView):
    """
    Обновление аватарки пользователя.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user_profile = UserProfile.objects.get(user=request.user)
        avatar = request.FILES.get("avatar")

        if not avatar:
            return Response(
                {"error": "Avatar is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user_profile.avatar:
            user_profile.avatar.src = avatar
            user_profile.avatar.alt = request.data.get(
                "avatar_alt", user_profile.avatar.alt
            )
            user_profile.avatar.save()
        else:
            new_avatar = ProfileAvatar.objects.create(
                src=avatar, alt=request.data.get("avatar_alt", "")
            )
            user_profile.avatar = new_avatar
            user_profile.save()

        serializer = ProfileUserSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePasswordView(APIView):
    """
    Обновление пароля пользователя

    (Не рабочий, фронт не отправляет пароль.)
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user = request.user
        password = request.data.get("password")

        if not password:
            return Response(
                {"error": f"Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        return Response(status=status.HTTP_200_OK)
