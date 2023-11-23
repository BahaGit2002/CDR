from django.db import models


class CallStatus(models.TextChoices):
    successful = 'successful'
    unanswered = 'unanswered'
    rejected = 'rejected'


class CallType(models.TextChoices):
    outgoing = 'outgoing'
    incoming = 'incoming'
    missed = 'missed'
