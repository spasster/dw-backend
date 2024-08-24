from django.db import models
from enum import Enum
from django.utils import timezone
from datetime import timedelta


class Sub(Enum):
    MONTH = 30
    THREE_MONTHS = 90
    YEAR = 364 
    NONE = 0

    @classmethod
    def get_choices(cls):
        return [(i.name, i.value) for i in cls]
    
    
class SubscriptionManager(models.Manager):
    def create_sub(self, user_id, subType=Sub.NONE.value,  **extra_fields):
        statistics = self.model(
            user=user_id,
            subType=subType,
            **extra_fields
        )
        statistics.save(using=self._db)
        return statistics
    
class Subscription(models.Model):
    user = models.OneToOneField('authorization.DwUser', on_delete=models.CASCADE, primary_key=True)
    sub_type = models.IntegerField(
        choices=Sub.get_choices(),
        default=Sub.NONE.value
    )
    start_date = models.DateTimeField(default=None, null=True)
    expiration_date = models.DateTimeField(default=None, null=True)
    updated_at =  models.DateTimeField(auto_now=True)

    objects = SubscriptionManager()

    def purchase_subscription(self, sub_type):
        """Логика покупки подписки"""
        self.SubType = sub_type

        if sub_type == Sub.NONE.value:
            self.StartDate = None
            self.ExpirationDate = None
        else:
            if self.StartDate is None:
                self.StartDate = timezone.now()
            if self.ExpirationDate is None or self.ExpirationDate < timezone.now():
                self.ExpirationDate = self.StartDate + timedelta(days=sub_type)
            else:
                self.ExpirationDate += timedelta(days=sub_type)
        self.save()

