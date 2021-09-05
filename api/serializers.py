from rest_framework import serializers

from .models import User, UserData, Winner


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        exclude = ['token']


class WinnerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Winner
        fields = ['user', 'date']

    def get_user(self, obj):

        serializer = UserSerializer(obj.user)
        return serializer.data
