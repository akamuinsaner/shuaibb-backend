from gettext import install
import secrets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import User;
from users.backends import EmailAndMobileBackend
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import  ParseError, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Q

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


class UserListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=UserSerializer
    
    def get_queryset(self):
        list = User.objects.all()
        name = self.request.GET.get("name")
        roles = self.request.GET.get("roles")
        if name != None:
            list = list.filter(Q(username__contains=name) | Q(mobile__contains=name) | Q(email__contains=name))
        if (roles != None and len(roles) > 0):
            list = list.filter(role__in=roles.split(','))
        return list

    def create(self, request, *args, **kwargs):
        password = secrets.token_hex()
        data = request.data
        data["password"] = password
        serializer = UserSerializer(data=data)
        if (serializer.is_valid()):
            instance = serializer.save()
            groups = request.data.get('groups')
            if (groups is not None):
                groups = Group.objects.filter(id__in=groups)
                instance.groups.set(groups)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(serializer.errors)

user_list_view = UserListView.as_view()

class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=UserSerializer

    def get_object(self):
        return User.objects.get(pk=self.kwargs["id"])

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        groups = self.request.data.get('groups')
        if (groups is not None):
            groups = Group.objects.filter(id__in=groups)
            instance.groups.set(groups)

    def perform_destroy(self, instance):
        if (instance == self.request.user):
            raise ValidationError('不能删除自己')
        instance.delete()

user_detail_view = UserDetailView.as_view()



