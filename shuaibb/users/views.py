from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from users.backends import EmailAndMobileBackend
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import  ParseError, ValidationError

class SignUpView(APIView):
    def post(self, request):
        validate_data = request.data
        validate_data["password"] = make_password(validate_data.get("password"))
        serializer = UserSerializer(data = validate_data)
        if (validate_data["login_type"] == 'mobile' and validate_data["mobile"] == None):
            raise ValidationError('手机号不能为空')
        if (validate_data["login_type"] == 'email' and validate_data["email"] == None):
            raise ValidationError('邮箱不能为空')
        if (serializer.is_valid()):
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        else:
            raise ParseError(detail="参数错误")

sign_up_view = SignUpView.as_view()

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if (serializer.is_valid()):
            mobile = serializer.validated_data.get('mobile')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = None
            if (mobile is not None):
                user = EmailAndMobileBackend.authenticate(self, request, username=None, password=password, mobile=mobile)
            if (email is not None):
                user = EmailAndMobileBackend.authenticate(self, request, username=None, password=password, email=email)
            token = Token.objects.get(user=user)
            return Response(token.key, status = status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors)
        #raise ParseError(detail="参数错误")

login_view = LoginView.as_view()

class UserByToken(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        token = request.auth
        user = Token.objects.get(key = token).user
        
        if (user is not None):
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

user_by_token = UserByToken.as_view()




