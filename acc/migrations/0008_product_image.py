# Generated by Django 4.0.2 on 2022-02-23 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0007_alter_user_role_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to='images/'),
        ),
    ]
