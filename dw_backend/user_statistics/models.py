from django.db import models
from datetime import timedelta


class RefferalManager(models.Manager):
    def create_refferal(self, user_id, refferalAvailable=False, **extra_fields):
        if not refferalAvailable:
            code = None
            refferalNumber = None
            refferalBonus = None

        refferal = self.model(
            user=user_id,
            refferalAvailable=refferalAvailable,
            code=code,
            refferalNumber=refferalNumber,
            refferalBonus=refferalBonus,
            **extra_fields
        )

        refferal.save(using=self._db)
        return refferal

class RefferalSystem(models.Model):
    user = models.OneToOneField('authorization.DwUser', on_delete=models.CASCADE, primary_key=True)
    refferalAvailable = models.BooleanField(default=False)

    code = models.CharField(max_length=50, null=True)
    refferalNumber = models.IntegerField(null=True)
    refferalBonus = models.IntegerField(null=True)

    objects = RefferalManager()



class StatisticsManager(models.Manager):
    def create_statistics(self, user_id, last_login=None,  **extra_fields):
        statistics = self.model(
            user=user_id,
            last_login=last_login,
            **extra_fields
        )
        statistics.save(using=self._db)
        return statistics

class Statistics(models.Model):
    user = models.OneToOneField('authorization.DwUser', on_delete=models.CASCADE, primary_key=True)
    reg_date = models.DateTimeField(auto_now_add=True) 
    last_login = models.DateTimeField(null=True) 
    launch_number = models.IntegerField(default=0)
    playtime = models.DurationField(default=timedelta()) 

    avatar = models.ImageField(upload_to='avatars/', null=True)

    objects = StatisticsManager()

    def display_playtime_in_minutes(self):
        total_minutes = int(self.playtime.total_seconds() // 60)
        return total_minutes
