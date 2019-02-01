# Generated by Django 2.1.5 on 2019-01-31 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakfasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breakfast',
            name='is_recursive',
            field=models.BooleanField(default=True, verbose_name='is recursive'),
        ),
        migrations.AddField(
            model_name='participant',
            name='notif',
            field=models.BooleanField(default=True, verbose_name='receive email notification'),
        ),
    ]