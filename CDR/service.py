import random
from CDR.models import User
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives


class UserAuthService:
    """Service for handling AUTH methods"""

    @classmethod
    def get_response(cls, user, email) -> Response:
        """Method для login или создания пользователя и отсылки SMS """
        if not cls.send_confirmation_sms(user, email):
            return Response(
                {
                    'message': _(
                        'Не удалось отправить сообщение. Попробуйте позже.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'message': _('Сообщение отправлено')}, status=status.HTTP_200_OK
        )

    @staticmethod
    def generate_new_code():
        """Method for generating random confirmation code"""
        code = str(random.randint(1000, 9999))
        return code

    @staticmethod
    def compare_confirmation_time(user_obj) -> bool:
        """ Method for checking if 1 minute left from last request """
        if not user_obj.confirmation_date:
            return True
        prite = timezone.now() - user_obj.confirmation_date
        if prite > timedelta(minutes=2):
            return True
        else:
            return False

    @classmethod
    def set_confirmation_code(cls, user_obj: User) -> str:
        """Method for setting confirmation sms code to user"""
        confirmation_code = cls.generate_new_code()
        user_obj.confirmation_code = confirmation_code
        user_obj.confirmation_date = timezone.now() + timedelta(minutes=5)
        user_obj.save(
            update_fields=['confirmation_code', 'confirmation_date']
        )
        return confirmation_code

    @classmethod
    def send_confirmation_sms(cls, user_obj, email) -> bool:
        """Method for sending confirmation sms to new user"""
        confirmation_code = cls.set_confirmation_code(user_obj)

        cls.send_email(int(confirmation_code), email)
        return True



    @staticmethod
    def send_email(code, email):
        html = f"<span>Код для подтверждения почты<span> <h2>{code}<h2>"
        email = EmailMultiAlternatives(
            subject='Подтверждение почты', body=html, to=[email]
        )
        email.attach_alternative(html, "text/html")
        email.send()
