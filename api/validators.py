from rest_framework import serializers

from .models import User


def check_email(email):
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return email

    raise serializers.ValidationError(detail={'error': 'ya existe una cuenta con ese email'})
