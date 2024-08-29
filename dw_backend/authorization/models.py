from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.exceptions import ValidationError

from subscription.models import Subscription
from user_statistics.models import RefferalSystem
from user_statistics.models import Statistics
from authorization.enums import Role

class DwUserManager(BaseUserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.MANAGER.value)

        if extra_fields.get('role') != Role.MANAGER.value:
            raise ValueError('Superuser must have role=MANAGER.')

        return self.create_user(username=username, password=password, **extra_fields)

    def create_user(self, username, email=None, password=None, hwid=None, role=Role.VISITOR.value, **extra_fields):
        print(username, password)
        user = self.model(
            username=username,
            email=email,
            hwid=hwid,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        # Создание связанных записей
        Subscription.objects.create_sub(user_id=user)
        RefferalSystem.objects.create_refferal(user_id=user)
        Statistics.objects.create_statistics(user_id=user)

        return user


class DwUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    hwid = models.TextField(null=True)
    role = models.CharField(max_length=50, choices=Role.get_choices(), default=Role.USER.value)

    last_login = None

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    objects = DwUserManager()

    def set_hwid(self, hwid_value):
        if self.hwid is not None:
            raise ValidationError("HWID can only be set once and cannot be changed.")
        self.hwid = hwid_value
        self.save()

    def admin_update_hwid(self, hwid_value):
        self.hwid = hwid_value
        self.save()

    @property
    def is_staff(self):
        return self.role in [Role.MANAGER.value, Role.CEO.value]

    @property
    def is_superuser(self):
        return self.role in [Role.MANAGER.value, Role.CEO.value]

