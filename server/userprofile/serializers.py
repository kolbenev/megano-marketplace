from rest_framework import serializers
from userprofile.models import UserProfile


class ProfileUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(method_name="get_avatar")

    class Meta:
        model = UserProfile
        fields = ['fullName', 'email', 'phone', 'avatar']

    def get_avatar(self, obj):
        try:
            return {"src": obj.avatar.src.url, "alt": obj.avatar.alt}
        except ValueError:
            return {"src": "/media/images/standart/standart-avatar.png", "alt": "Standard Avatar"}

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
