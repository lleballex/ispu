from .utils import encode_auth_token
from works.serializers import UserWorkListSerializer
from .models import User, TeacherProfile
from .serializers import UserSerializer, CreateStudentSerializer, \
                         CreateTeacherSerializer, PublicTeacherSerializer, \
                         CreateUserSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.exceptions import ParseError, PermissionDenied


class LoginView(APIView):
    def get(self, request: Request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return Response(UserSerializer(request.user).data)

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            raise ParseError('Username is not specified')
        if not password:
            raise ParseError('Password is not specified')

        user = User.objects.get(username=username)

        if user.temp_password:
            if user.password != password:
                user = None
        else:
            user = authenticate(username=username, password=password)

        if not user:
            raise ParseError('Username or password is invalid')

        return Response({
            'token': encode_auth_token(user.id),
            'user': UserSerializer(user).data,
        })


class RegisterUserView(CreateModelMixin, GenericAPIView):
    serializer_class = CreateUserSerializer

    # def get_serializer_class(self):
        # role = self.request.data.get('role')
    
        # if role == 'student':
            # return CreateStudentSerializer
        # elif role == 'teacher':
            # return CreateTeacherSerializer
        # else:
            # raise ParseError('Wrong role is specified')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)





class TeachersView(ListModelMixin, GenericAPIView):
    queryset = User.objects.filter(teacher_profile__isnull=False)
    serializer_class = PublicTeacherSerializer
    
    def get(self, request):
        return self.list(request)


class UserWorksView(ListModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]      # TODO: only for author or teacher
    serializer_class = UserWorkListSerializer

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        try:
            self.request.user.student_profile
        except:
            pass
        else:
            return self.request.user.student_profile.works.all()

        try:
            self.request.user.teacher_profile
        except:
            pass
        else:
            return self.request.user.teacher_profile.works.all()

        return []
