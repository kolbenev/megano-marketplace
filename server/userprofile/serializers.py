from rest_framework import serializers

from userprofile.models import UserProfile

from rest_framework import serializers
from .models import UserProfile


class ProfileUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(method_name="get_avatar")

    class Meta:
        model = UserProfile
        fields = ['fullName', 'email', 'phone', 'avatar']

    def get_avatar(self, obj):
        return {"src": obj.avatar_src.url if obj.avatar_src else None, "alt": obj.avatar_alt}

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)

        if 'avatar' in validated_data:
            avatar_data = validated_data.get('avatar')
            instance.avatar_src = avatar_data.get('src', instance.avatar_src)
            instance.avatar_alt = avatar_data.get('alt', instance.avatar_alt)

        instance.save()
        return instance
