from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status


from authorization.models import DwUser
from authorization.serializers import DwUserSerializer
from authorization.serializers import CustomAuthTokenSerializer


logger = logging.getLogger('authorization')


class RegistrationViewSet(viewsets.ModelViewSet):
    """Онли регистрация"""

    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = DwUser.objects.all()
    serializer_class = DwUserSerializer

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
        }, status=status.HTTP_200_OK)