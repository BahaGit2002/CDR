# Generated by Django 4.2.7 on 2023-11-22 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CDR', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdr',
            name='call_status',
            field=models.CharField(choices=[('successful', 'Successful'), ('unanswered', 'Unanswered'), ('rejected', 'Rejected')], max_length=20),
        ),
        migrations.AlterField(
            model_name='cdr',
            name='call_type',
            field=models.CharField(choices=[('outgoing', 'Outgoing'), ('incoming', 'Incoming'), ('missed', 'Missed')], max_length=20),
        ),
    ]
