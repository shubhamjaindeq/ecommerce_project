# Generated by Django 4.0.2 on 2022-02-22 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0006_user_shopaddress_user_shopdesc_user_shopname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(max_length=10),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('brand', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('electronics', 'electronics'), ('footwear', 'footwear'), ('accesories', 'accesories')], max_length=50)),
                ('quantity', models.IntegerField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
