from .models import User, StudentProfile, TeacherProfile

from django.db import transaction
from rest_framework.serializers import CharField, ModelSerializer, \
                                       SerializerMethodField


class StudentProfileSerializer(ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'number', 'course', 'group']


class TeacherProfileSerializer(ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['id']


class UserSerializer(ModelSerializer):
    student_profile = StudentProfileSerializer()
    teacher_profile = TeacherProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'patronymic',
                  'student_profile', 'teacher_profile']


class CreateUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'patronymic']

    @transaction.atomic()
    def create(self, validated_data):
        validated_data['temp_password'] = False
        return User.objects.create_user(**validated_data)


class CreateStudentSerializer(ModelSerializer):
    password = CharField(write_only=True)
    student_profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name',
                  'student_profile']

    @transaction.atomic()
    def create(self, validated_data):
        profile = validated_data.pop('student_profile')
        profile_serializer = StudentProfileSerializer(data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        validated_data['student_profile'] = StudentProfile.objects.get(
            id=profile_serializer.data['id'])

        return User.objects.create_user(**validated_data)


class CreateTeacherSerializer(ModelSerializer):
    password = CharField(write_only=True)
    teacher_profile = TeacherProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name',
                  'teacher_profile']

    @transaction.atomic()
    def create(self, validated_data):
        profile = validated_data.pop('teacher_profile')
        profile_serializer = TeacherProfileSerializer(data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        validated_data['teacher_profile'] = TeacherProfile.objects.get(
            id=profile_serializer.data['id'])

        return User.objects.create_user(**validated_data)


class PublicTeacherSerializer(ModelSerializer):
    teacher_id = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'teacher_id']

    def get_teacher_id(self, value):
        return value.teacher_profile.id


class PublicStudentSerializer(ModelSerializer):
    student_id = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'student_id']

    def get_student_id(self, value):
        return value.student_profile.id


class PublicUserSerialzier(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'patronymic']
