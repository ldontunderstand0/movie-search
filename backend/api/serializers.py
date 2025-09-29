from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
)
from . import models


class SignUpSerializer(ModelSerializer):
    password1 = CharField(
        write_only=True,
        required=True,
        max_length=100,
        validators=[validate_password])
    password2 = CharField(
        write_only=True,
        required=True,
        max_length=100,
        validators=[validate_password])

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password1', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        validated_data['password'] = password
        instance = self.Meta.model(**validated_data)

        instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password']


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']

