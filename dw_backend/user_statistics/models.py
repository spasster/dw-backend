from django.db import models
from authorization.models import DwUser


class RefferalManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class RefferalSystem(models.Model):
    user_id = models.ForeignKey(DwUser, null=True, on_delete=models.SET_NULL)
    refferalAvailable = models.BooleanField(default=False)

    code = models.CharField(max_length=50)
    refferalNumber = models.IntegerField(default=0)
    refferalBonus = models.IntegerField(default=0)

    objects = RefferalManager()


class StatisticsManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class Statistics(models.Model):
    user_id = models.ForeignKey(DwUser, null=True, on_delete=models.SET_NULL)
    regDate = models.DateTimeField(auto_now_add=True)

    launchNumber = models.IntegerField(default=0)
    refferalNumber = models.IntegerField(default=0)
    refferalBonus = models.IntegerField(default=0)

    objects = RefferalManager()