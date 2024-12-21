from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.serializers import ProfileUserSerializer
from userprofile.models import UserProfile


class ProfileGetAPIView(APIView):
    def get(self, request: Request) -> Response:
        permission_classes = (IsAuthenticated,)
        profile = UserProfile.objects.get(user=request.user)
        serializer = ProfileUserSerializer(profile)
        return Response(serializer.data)


class ProfilePostAPIView(APIView):
    """
    Эндпоинт для обновления информации о профиле пользователя.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = ProfileUserSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAvatarView(APIView):
    """
    Эндпоинт для обновления аватара пользователя.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request: Request) -> Response:
        user_profile = UserProfile.objects.get(user=request.user)
        avatar = request.FILES.get('avatar')

        if not avatar:
            return Response({"error": "Avatar is required."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.avatar_src = avatar
        user_profile.avatar_alt = request.data.get('avatar_alt', user_profile.avatar_alt)
        user_profile.save()

        serializer = ProfileUserSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePasswordView(APIView):
    """
    Эндпоинт для обновления пароля пользователя.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user = request.user
        password = request.data.get('password')

        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)