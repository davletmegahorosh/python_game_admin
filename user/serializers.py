import base64
import uuid
import os
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from .models import CustomUser
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password


class Base64ImageField(serializers.ImageField):
    """
    Serializer field for handling base64 encoded images.
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[-1]
                decoded_data = base64.b64decode(imgstr)

                # Генерируем уникальное имя файла
                file_name = f"{uuid.uuid4()}.{ext}"
                output_file_path = os.path.join('media', 'avatars', file_name)

                # Сохраняем файл на диск
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decoded_data)

                # Формируем URL для доступа к файлу
                file_url = os.path.join('avatars', file_name)

                return {'file_name': file_name, 'file_url': file_url}  # возвращаем имя и URL файла

            except (TypeError, ValueError, base64.binascii.Error) as e:
                raise ValidationError("Invalid base64 data")
        else:
            return super().to_internal_value(data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    # avatar = Base64ImageField(write_only=True, required=False)  # Используем Base64ImageField
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        validators=[
            RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.'),
            UniqueValidator(queryset=CustomUser.objects.all(), message='This username is already in use.')
        ]
    )
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'confirmation_code', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        if validate_password(data) is not None:
            raise serializers.ValidationError("Password min length is 8")
        return data

    def create(self, validated_data):
        avatar_data = validated_data.pop('avatar', None)
        confirmation_code = get_random_string(length=4, allowed_chars='0123456789')
        validated_data['confirmation_code'] = confirmation_code

        # Создаем объект пользователя
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_active=True,
            confirmation_code=confirmation_code,
        )

        # if avatar_data:
        #     user.avatar = avatar_data['file_url']  # Сохраняем URL аватара в объекте пользователя
        #     user.save()  # Сохраняем изменения в базе данных

        return {
            'username': user.username,
            'email': user.email,
            # 'avatar_url': avatar_data['file_url'] if avatar_data else None,  # Возвращаем URL аватара
            'confirmation_code': user.confirmation_code,
        }
