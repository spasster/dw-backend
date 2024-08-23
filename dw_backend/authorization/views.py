from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import logging


from authorization.models import DwUser
from authorization.serializers import DwUserSerializer


logger = logging.getLogger('authorization')


class RegistrationViewSet(viewsets.ModelViewSet):
    """Онли регистрация"""

    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = DwUser.objects.all()
    serializer_class = DwUserSerializer

    def post(self, request, *args, **kwargs):
        logger.info("НАЧАЛО ПОСТА")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Ответ: {response}")
        user = DwUser.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
class GetViewSet(viewsets.ModelViewSet):
    """Получение всех юзеров"""

    queryset = DwUser.objects.all()
    serializer_class = DwUserSerializer
