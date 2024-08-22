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
        extra_fields.setdefault('role', Role.MANAGER.value)

        if extra_fields.get('role') != Role.CEO.value:
            raise ValueError('Superuser must have role=CEO.')

        return self.create_user(username, password, **extra_fields)
    
    def create_user(self, username, email, password=None, hwid=None, role=None, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            hwid=hwid,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class DwUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    
    hwid = models.TextField(null=True)
    role = models.CharField(
        max_length=50,
        choices=Role.get_choices(),
        default=Role.USER.value
    )

    subId = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)


    last_login = None  #хуйня появляется из-за наследования от AbstractBaseUser так что убиваем


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    objects = DwUserManager()
