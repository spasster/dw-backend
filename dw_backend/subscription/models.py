from django.db import models
from enum import Enum
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
import random
import string

from authorization.enums import Role
from subscription.enums import Sub
    
    
class SubscriptionKeyManager(models.Manager):
    def activate_sub_key(self, user, key=None, **extra_fields):
        """Create a subscription by key activation"""

        sub = Subscription.objects.get(user = user)
        print(key)

        if key:
            # Update subscription details based on key
            key_obj = SubscriptionKey.objects.filter(key=key).first()
            if not key_obj:
                raise ValidationError("Invalid or expired key.")

            sub.add_subscription(key_obj.sub_dur)
            key_obj.delete() 

class SubscriptionManager(models.Manager):
    def create_sub(self, user_id, sub_dur=Sub.NONE.value,  **extra_fields):
        statistics = self.model(
            user=user_id,
            sub_dur=sub_dur,
            **extra_fields
        )
        statistics.save(using=self._db)
        return statistics
    
class Subscription(models.Model):
    user = models.OneToOneField('authorization.DwUser', on_delete=models.CASCADE, primary_key=True)
    sub_dur = models.IntegerField(
        choices=Sub.get_choices(),
        default=Sub.NONE.value
    )
    start_date = models.DateTimeField(default=None, null=True)
    expiration_date = models.DateTimeField(default=None, null=True)
    updated_at =  models.DateTimeField(auto_now=True)

    objects = SubscriptionManager()

    def add_subscription(self, sub_dur):
        """добавление подписки подписки"""

        try:
            sub_enum = Sub[sub_dur] 
        except KeyError:
            raise ValidationError(f"Invalid subscription duration: {sub_dur}")

        self.sub_dur = sub_enum.value 

        if sub_enum == Sub.NONE:
            self.start_date = None
            self.expiration_date = None
        else:
            if self.start_date is None:
                self.start_date = timezone.now()
            if self.expiration_date is None or self.expiration_date < timezone.now():
                self.expiration_date = self.start_date + timedelta(days=sub_enum.value)
            else:
                self.expiration_date += timedelta(days=sub_enum.value)

        if self.user.role == Role.VISITOR.value:
            self.user.role = Role.USER.value
            self.user.save()

        self.save()


class SubscriptionKey(models.Model):

    key = models.CharField(max_length=255, unique=True)
    sub_dur = models.CharField(max_length=50, choices=Sub.get_choices())
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    objects = SubscriptionKeyManager()  # Стандартный менеджер

    def is_valid(self):
        """Check if the key is still valid based on its expiration date and activation status."""
        now = timezone.now()
        return self.is_active and (self.expires_at is None or self.expires_at > now)

    def __str__(self):
        return self.key
    
    @staticmethod
    def generate_key(prefix="drainwalk_", length=16):
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return f"{prefix}{suffix}"


