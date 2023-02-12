from .utils import encode_auth_token
from .serializers import UserSerializer, CreateStudentSerializer, \
                         CreateTeacherSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView


class LoginView(APIView):
    def get(self, request: Request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return Response(UserSerializer(request.user).data)

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            raise ParseError('Email is not specified')
        if not password:
            raise ParseError('Password is not specified')

        user = authenticate(email=email, password=password)

        if not user:
            raise ParseError('Email or password is invalid')

        return Response({
            'token': encode_auth_token(user.id),
            'user': UserSerializer(user).data,
        })


class RegisterUserView(CreateModelMixin, GenericAPIView):
    def get_serializer_class(self):
        role = self.request.data.get('role')
    
        if role == 'student':
            return CreateStudentSerializer
        elif role == 'teacher':
            return CreateTeacherSerializer
        else:
            raise ParseError('Wrong role is specified')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
