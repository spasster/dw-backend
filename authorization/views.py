from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from django.conf import settings
import requests

from authorization.models import DwUser
from authorization.serializers import DwUserSerializer
from authorization.serializers import CustomAuthTokenSerializer


logger = logging.getLogger('authorization')


class RegistrationViewSet(viewsets.ModelViewSet):
    """Регистрация с проверкой Cloudflare Turnstile"""

    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = DwUser.objects.all()
    serializer_class = DwUserSerializer

    def create(self, request, *args, **kwargs):
        # Получаем токен капчи с фронтенда
        turnstile_token = request.data.get('token')
        print(turnstile_token)
        # Проверяем, передан ли токен
        if not turnstile_token:
            return Response({'error': 'CAPTCHA token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем капчу через API Cloudflare
        captcha_valid = self.verify_turnstile(turnstile_token)
        if not captcha_valid:
            return Response({'error': 'CAPTCHA validation failed'}, status=status.HTTP_400_BAD_REQUEST)

        # Если капча прошла проверку, продолжаем регистрацию
        return self.create_user(request, *args, **kwargs)

    def verify_turnstile(self, token):
        """Проверка капчи через API Cloudflare"""
        url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        secret_key = settings.CLOUDFLARE_TURNSTILE_SECRET_KEY 
        data = {
            'secret': secret_key,
            'response': token
        }

        try:
            response = requests.post(url, data=data)
            result = response.json()
            return result.get('success', False)
        except requests.RequestException:
            return False

    def create_user(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = DwUser.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class CustomAuth(TokenObtainPairView):
    """Кастомная авторизация так как сразу два поля могут быть логином"""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request):
        logger.info("НАЧАЛО ПОСТА")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = serializer.get_token(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': str(user.username)
        }, status=status.HTTP_200_OK)
    
class SetHWIDView(APIView):
    """Установка хвхида при первом запуске"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        hwid_value = request.data.get('hwid')

        user = get_object_or_404(DwUser, id=request.user.id)

        try:
            user.set_hwid(hwid_value)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "HWID set successfully."}, status=status.HTTP_200_OK)
    

class ChangePasswordView(generics.UpdateAPIView):
    """
    Позволяет аутентифицированному пользователю изменить свой пароль.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Пароль введен неверно."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"success": "Пароль успешно изменен."}, status=status.HTTP_200_OK)