# Generated by Django 2.1.4 on 2019-01-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_breakfasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
    ]