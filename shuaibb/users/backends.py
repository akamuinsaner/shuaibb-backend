from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model


class EmailAndMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        mobile = kwargs.get('mobile')
        email = kwargs.get('email')
        user = None
        if (username is not None):
            user = UserModel.objects.get(username=username)
        if (mobile is not None):
            user = UserModel.objects.get(mobile=mobile)
        if (email is not None):
            user = UserModel.objects.get(email=email)
        if user.check_password(password):
            return user
