import logging
from os import stat

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login as django_login
import django.core.exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from itsdangerous import URLSafeTimedSerializer
from rest_auth.views import LoginView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import UserSerializer

from common.utils import get_client_ip
logger = logging.getLogger(__name__)
serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="bluewhale2021")
UserModel = get_user_model()


def generate_token(data):
    return serializer.dumps(str(data))


def validate_token(token):
    if not token:
        return None
    max_token_age = settings.REGISTER_TOKEN_TTL
    try:
        return serializer.loads(token, max_age=max_token_age)
    except Exception as e:
        logger.exception(e)
        return None


class BluewhaleLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})

        try:
            # the real authenticate process
            # please refer to `rest_auth.serializer.LoginSerializer`
            self.serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.error(e)
            return Response({"data": None, "code": 0}, status=status.HTTP_401_UNAUTHORIZED)
        user = self.serializer.validated_data['user']
        user.last_login_ip = get_client_ip(request)

        self.login()
        user.save(update_fields=['last_login_ip'])
        serializer = UserSerializer(user)
        return Response({"data": serializer.data, "code": 0})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response({"data": serializer.data, "code": 0})
    else:
        return Response({"data": None, "code": 0}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def send_verification_mail(request):
    data = request.data
    email = data.get('email')
    try:
        validate_email(email)
        user = UserModel.objects.filter(email=email).first()
        if user:
            return Response({"data": None, "code": 409, "message": "Email has been registered"}, status=status.HTTP_409_CONFLICT)
    except django.core.exceptions.ValidationError as e:
        logger.error(e)
        return Response({"data": None, "code": 400, "message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
    token = generate_token(email)
    message = f'Click following link to verify your email address: {settings.SITE_HOST}/verify/{token}'
    result = send_mail(
        _("Please verify your email address"),
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )
    return Response({"data": result, "code": 0})


@api_view(['GET'])
def verify_verification_token(request, token):
    email = validate_token(token)
    if not email:
        return Response({"data": None, "code": 400}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"data": email, "code": 0})

@api_view(['POST'])
def register(request):
    data = request.data
    email = validate_token(data.get('token'))
    if not email:
        return Response({"data": None, "code": 400, "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    password = data.get('password')
    if not password:
        return Response({"data": None, "code": 400, "message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_password(password)
    except django.core.exceptions.ValidationError as e:
        logger.error(e)
        return Response({"data": None, "code": 400, "message": e.messages}, status.HTTP_400_BAD_REQUEST)
    user = UserModel.objects.filter(email=email).first()
    if user:
        return Response({"data": None, "code": 409, "message": "Email has been registered"}, status=status.HTTP_409_CONFLICT)
    user = UserModel(email=email, phone=None)
    user.set_password(password)
    user.save()
    django_login(request, user)
    return Response({"data": UserSerializer(user).data, "code": 0}, status=status.HTTP_201_CREATED)
