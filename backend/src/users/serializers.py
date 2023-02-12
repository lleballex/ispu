from .models import User, StudentProfile, TeacherProfile

from django.db import transaction
from rest_framework.serializers import CharField, ModelSerializer


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
        fields = ['email', 'first_name', 'last_name', 'student_profile',
                  'teacher_profile']


class CreateStudentSerializer(ModelSerializer):
    password = CharField(write_only=True)
    student_profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name',
                  'student_profile']

    @transaction.atomic
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

    @transaction.atomic
    def create(self, validated_data):
        profile = validated_data.pop('teacher_profile')
        profile_serializer = TeacherProfileSerializer(data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        validated_data['teacher_profile'] = TeacherProfile.objects.get(
            id=profile_serializer.data['id'])

        return User.objects.create_user(**validated_data)
