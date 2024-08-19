from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from enum import Enum


class Role(Enum):
    CEO = 'CEO'
    MANAGER = 'MANAGER'
    BETA = 'BETA'
    USER = 'USER'
    MEDIA = 'MEDIA'
    VISITOR = 'VISITOR'
    DEACTIVATED = 'AZIK'

    @classmethod
    def get_choices(cls):
        return [(i.name, i.value) for i in cls]


class Sub(Enum):
    WEEK = 7 # 7 days in a week
    MONTH = 30 # Approximately 30 days in a month
    THREE_MONTHS = 90 # Approximately 90 days in three months
    HALF_A_YEAR = 182 # Approximately 182 days in half a year
    NONE = 0

    @classmethod
    def get_choices(cls):
        return [(i.name, i.value) for i in cls]


class DwUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class DwUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50,
        choices=Role.get_choices(),
        default=Role.USER.name
    )
    sub = models.IntegerField(
        choices=Sub.get_choices(),
        default=Sub.NONE.value
    )
    sub_until = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    objects = DwUserManager()
