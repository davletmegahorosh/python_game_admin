from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .models import CustomUser

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data.get('email'),
                password=data['password'],
                is_active=True,
            )
            confirmation_code = get_random_string(length=4, allowed_chars='0123456789')
            user.confirmation_code = confirmation_code
            user.save()

            response_data = {
                'username': user.username,
                'email': user.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
