from django.db import models
from enum import Enum
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError


class Sub(Enum):
    MONTH = 30
    THREE_MONTHS = 90
    YEAR = 364 
    NONE = 0

    @classmethod
    def get_choices(cls):
        return [(i.name, i.value) for i in cls]
    
    
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
        self.save()

