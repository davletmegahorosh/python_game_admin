import base64
import random
import uuid
import os

from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.conf import settings


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(write_only=True, required=False, allow_blank=True)  # base64 encoded image (not required)
    confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'avatar', 'confirmation_code')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        avatar_base64 = validated_data.pop('avatar', None)

        confirmation_code = random.randint(100000, 999999)

        validated_data['confirmation_code'] = confirmation_code

        if avatar_base64:
            format, imgstr = avatar_base64.split(';base64,')
            ext = format.split('/')[-1]
            avatar = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
            validated_data['avatar'] = avatar

        validated_data['password'] = make_password(validated_data['password'])

        user = CustomUser.objects.create(**validated_data)

        return user
