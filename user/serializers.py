import base64
import uuid

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from .models import CustomUser
from django.utils.crypto import get_random_string
# from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.'),
                    UniqueValidator(queryset=CustomUser.objects.all(), message='This username is already in use.')]
    )
    email = serializers.EmailField()


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'confirmation_code', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        if validate_password(data) is not None:
            raise serializers.ValidationError("Password min length is 8")
        return data

    def create(self, validated_data):
        avatar_base64 = validated_data.pop('avatar', None)
        confirmation_code = get_random_string(length=4, allowed_chars='0123456789')
        validated_data['confirmation_code'] = confirmation_code

        if avatar_base64:
            format, imgstr = avatar_base64.split(';base64,')
            ext = format.split('/')[-1]
            avatar = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
            validated_data['avatar'] = avatar

        validated_data['password'] = make_password(validated_data['password'])


        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_active=False,
            confirmation_code=confirmation_code,
        )

        return user

        # subject = 'Confirmation code'
        # message = f'Your confirmation code is: {confirmation_code}'
        # from_email = 'bapaevmyrza038@gmail.com'
        # recipient_list = [user.email]
        #
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)