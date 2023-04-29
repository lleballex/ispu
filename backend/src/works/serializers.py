from rest_framework.permissions import SAFE_METHODS
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Work, TasksCategory, FieldCategory, Comment
from users.serializers import PublicTeacherSerializer, PublicStudentSerializer, PublicUserSerialzier



class TasksCategorySerializer(ModelSerializer):
    class Meta:
        model = TasksCategory
        fields = ['id', 'name']


class FieldCategorySerializer (ModelSerializer):
    class Meta:
        model = FieldCategory 
        fields = ['id', 'name']


class CommentSerializer(ModelSerializer):
    user = PublicUserSerialzier()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'work', 'text', 'replies']
        read_only_fields = ['replies']

    # def to_representation(self, instance):
        # data = super().to_representation(instance)
        # if self.context['request'].method in SAFE_METHODS:
            # data['user'] = PublicUserSerialzier(data['user']).data
        # return data


class CreateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'work', 'text']


class WorkSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Work
        fields = ['id', 'name', 'student', 'author', 'teacher', 'issue', 'novelty',
                  'field', 'tasks', 'significance', 'tools', 'aprobation',
                  'keywords', 'status', 'comments', 'likes',
                  'is_liked', 'message',
                  'tasks_category', 'field_category'] # TODO: message only for teacher review
        read_only_fields = ['message']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].method in SAFE_METHODS:
            data['student'] = PublicStudentSerializer(instance.student.user).data
        return data

    def get_likes(self, value):
        return value.liked_users.count()

    def get_is_liked(self, value):
        return bool(value.liked_users.filter(
            id=self.context['request'].user.id))


class UpdateWorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'name', 'author', 'teacher', 'issue', 'novelty',
                  'field', 'tasks', 'significance', 'tools', 'aprobation',
                  'keywords', 'tasks_category', 'field_category']

    def update(self, instance, validated_data):
        instance.status = 'PENDING'
        return super().update(instance, validated_data)


class WorkListSerializer(ModelSerializer):
    tasks_category = TasksCategorySerializer()
    field_category = FieldCategorySerializer()

    class Meta:
        model = Work
        fields = ['id', 'name', 'issue', 'tasks_category', 'field_category']


class UserWorkListSerializer(ModelSerializer):
    teacher = PublicTeacherSerializer(source='teacher.user')
    student = PublicStudentSerializer(source='student.user')

    class Meta:
        model = Work
        fields = ['id', 'name', 'teacher', 'student', 'status', 'message']


class ReviewWorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'status', 'message']
