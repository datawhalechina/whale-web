import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logging.info('auth username: %s' % username)
        UserModel = get_user_model()
        user = None
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(phone=username)
            except UserModel.DoesNotExist:
                return None
        if user and user.check_password(password):
            return user
        return None
