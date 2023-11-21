from django.db import models


class CDR(models.Model):
    call_id = models.AutoField(primary_key=True)
    calling_number = models.CharField(max_length=16)
    called_number = models.CharField(max_length=16)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    call_status = models.CharField(max_length=20)
    call_type = models.CharField(max_length=20)

