# Generated by Django 4.0.2 on 2022-02-28 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0015_remove_orderitems_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='provider',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
