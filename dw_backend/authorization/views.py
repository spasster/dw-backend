from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authorization.models import DwUser
from authorization.serializers import DwUserSerializer

# Create your views here.

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = DwUser.objects.all()
    serializer_class = DwUserSerializer

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = DwUser.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })