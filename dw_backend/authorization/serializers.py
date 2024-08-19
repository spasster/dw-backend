from rest_framework import serializers

from authorization.models import DwUser
from django.contrib.auth.hashers import make_password


class DwUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = DwUser
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = DwUser.objects.create(**validated_data, password=make_password(password))
        return user
