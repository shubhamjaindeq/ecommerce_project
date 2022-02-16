# Generated by Django 4.0.2 on 2022-02-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0003_remove_myuser_is_shop_user_myuser_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='roles',
        ),
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('shopowner', 'shopowner'), ('customer', 'customer')], default='customer', max_length=10),
        ),
    ]
