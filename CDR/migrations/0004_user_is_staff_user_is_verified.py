# Generated by Django 4.2.7 on 2023-11-22 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CDR', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
