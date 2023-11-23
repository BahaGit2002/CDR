from django.db import models
from CDR.choices import CallType, CallStatus
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class CDR(models.Model):
    call_id = models.AutoField(primary_key=True)
    calling_number = models.CharField(max_length=16)
    called_number = models.CharField(max_length=16)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    call_status = models.CharField(max_length=20, choices=CallStatus.choices)
    call_type = models.CharField(max_length=20, choices=CallType.choices)


class UserManager(BaseUserManager):
    def create_user(self, password, email=None, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))
        user = self.model(email=email, **extra_fields)
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(password, email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

