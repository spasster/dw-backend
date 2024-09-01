from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
import logging

from authorization.models import DwUser

logger = logging.getLogger('authorization')


class DwUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = DwUser
        fields = ['username', 'email', 'password', 'hwid', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'hwid': {'required': False},
            'role': {'required': False}
        }

    def create(self, validated_data):
        user = DwUser.objects.create_user(**validated_data)
        return user
    

class CustomAuthTokenSerializer(serializers.Serializer):

    login = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=True)

    def validate(self, attrs):

        login = attrs.get('login')
        password = attrs.get('password')

        if login and password:
            user = authenticate(request=self.context.get('request'), username=login, password=password)
            if not user:
                try:
                    user_obj = DwUser.objects.get(email=login)
                    user = authenticate(request=self.context.get('request'), username=user_obj.username, password=password)
                except DwUser.DoesNotExist:
                    raise AuthenticationFailed(_('Invalid username/email or password.'))

            if not user:
                logger.info("нихуя не подошло")
                raise AuthenticationFailed(_('Invalid username/email or password.'))
            attrs['user'] = user
        else:
            raise serializers.ValidationError(_('Must include "username/email" and "password".'))

        return attrs

    def get_token(self, user):
        return RefreshToken.for_user(user)