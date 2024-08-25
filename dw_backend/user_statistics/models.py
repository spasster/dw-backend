from django.db import models
from datetime import timedelta


class RefferalManager(models.Manager):
    def create_refferal(self, user_id, refferal_available=False, **extra_fields):
        if not refferal_available:
            code = None
            refferal_number = None
            refferal_bonus = None

        refferal = self.model(
            user=user_id,
            refferal_available=refferal_available,
            code=code,
            refferal_number=refferal_number,
            refferal_bonus=refferal_bonus,
            **extra_fields
        )

        refferal.save(using=self._db)
        return refferal

class RefferalSystem(models.Model):
    user = models.OneToOneField('authorization.DwUser', on_delete=models.CASCADE, primary_key=True)
    refferal_available = models.BooleanField(default=False)

    code = models.CharField(max_length=50, null=True)
    refferal_number = models.IntegerField(null=True)
    refferal_bonus = models.IntegerField(null=True)

    objects = RefferalManager()

    def activate_refferal_system(self, code):
        self.refferal_available = True
        self.code = code
        self.refferal_number = 0
        self.refferal_bonus = 0
        self.save()



class StatisticsManager(models.Manager):

    def create_statistics(self, user_id, **extra_fields):
        statistics = self.model(
            user=user_id,
            **extra_fields
        )
        statistics.save(using=self._db)
        return statistics

class Statistics(models.Model):
    user = models.OneToOneField('authorization.DwUser', on_delete=models.CASCADE, primary_key=True)
    reg_date = models.DateTimeField(auto_now_add=True) 
    last_launch = models.DateTimeField(null=True, default=None) 
    launch_number = models.IntegerField(default=0)
    playtime = models.DurationField(default=timedelta()) 

    avatar = models.ImageField(upload_to='avatars/', null=True)

    objects = StatisticsManager()

    def display_playtime_in_minutes(self):
        total_minutes = int(self.playtime.total_seconds() // 60)
        return total_minutes
    
    def update_statistics(self, additional_playtime, increment_launches, new_last_launch):
        if additional_playtime:
            self.playtime += additional_playtime
        if increment_launches:
            self.launch_number += 1
        if new_last_launch:
            self.last_launch = new_last_launch
            
        self.save()
