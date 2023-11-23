from rest_framework import serializers
from CDR.models import CDR, User
from rest_framework.exceptions import ValidationError, AuthenticationFailed
import datetime
from CDR.service import UserAuthService
from django.contrib.auth.hashers import check_password


class CDRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDR
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


class VerifySerializer(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        fields = ('email', 'code')

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('Пользователь не существует.')
        if user.confirmation_code != code:
            raise ValidationError('Код указан неверно')
        if UserAuthService.compare_confirmation_time(user):
            raise ValidationError('Этот код уже недействителен')
        user.is_verified = True
        user.is_active = True
        user.confirmation_date = datetime.datetime.now()
        user.save()
        return {'token': user.tokens()}

    def to_representation(self, instance):
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Такой пользователь не существует')
        if not check_password(password, user.password):
            raise AuthenticationFailed('Не верный пароль или почта')
        if not user.is_active:
            raise AuthenticationFailed('Аккаунт не активный')
        if not user.is_verified:
            raise AuthenticationFailed('Почта не подтвержден')
        return {'token': user.tokens()}

    def to_representation(self, instance):
        return instance

