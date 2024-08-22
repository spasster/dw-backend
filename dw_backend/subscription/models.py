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
    def available(self):
        return self.filter(SubType=True)
    
class Subscription(models.Model):
    id = models.AutoField(primary_key=True)

    subType = models.IntegerField(
        choices=Sub.get_choices(),
        default=Sub.NONE.value
    )

    startDate = models.DateTimeField(default=timezone.now)

    sxpirationDate = models.DateTimeField(null=True, blank=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt =  models.DateTimeField(auto_now=True)

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

    objects = SubscriptionManager()

