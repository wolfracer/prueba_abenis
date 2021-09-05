from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)


class UserData(models.Model):

    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    token = models.CharField(max_length=150, blank=True, null=True)


class Winner(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
