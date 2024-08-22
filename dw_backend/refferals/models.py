from django.db import models


class RefferalManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class RefferalSystem(models.Model):
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