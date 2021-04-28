import logging

from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


logger = logging.getLogger(__name__)
UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'phone',
            'nickname',
            'date_joined',
            'last_login',
            'last_login_ip',
            'description',
            'groups',
        )
