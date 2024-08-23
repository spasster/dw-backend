# Generated by Django 5.1 on 2024-08-23 19:09

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefferalSystem',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('refferalAvailable', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=50, null=True)),
                ('refferalNumber', models.IntegerField(null=True)),
                ('refferalBonus', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('launch_number', models.IntegerField(default=0)),
                ('playtime', models.DurationField(default=datetime.timedelta(0))),
                ('avatar', models.ImageField(null=True, upload_to='avatars/')),
            ],
        ),
    ]
