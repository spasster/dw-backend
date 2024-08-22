from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from enum import Enum
from subscription.models import Subscription


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


class DwUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class DwUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    Email = models.EmailField(unique=True, null=False)
    Password = models.CharField(max_length=50)
    Username = models.CharField(max_length=50, unique=True)
    
    Hwid = models.TextField(null=True)
    role = models.CharField(
        max_length=50,
        choices=Role.get_choices(),
        default=Role.USER.value
    )

    SubId = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)

    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    objects = DwUserManager()
