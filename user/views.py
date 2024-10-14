from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = serializer.validated_data.get('confirmation_code', None)
            return Response({'message': 'User registered successfully', 'confirmation_code': confirmation_code}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else None
                    }
                })
            else:
                return Response({'error': 'Account is inactive, please activate your account'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
