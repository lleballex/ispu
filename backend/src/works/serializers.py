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
    replies = SerializerMethodField()
    reply_to = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'work', 'text', 'replies', 'reply_to']
        read_only_fields = ['replies']

    def get_replies(self, comment):
        if comment.reply_to:
            return []
        return CommentSerializer(comment.common_replies.all(), many=True).data

    def get_reply_to(self, comment):
        if comment.reply_to:
            return f'{comment.reply_to.user.first_name} {comment.reply_to.user.last_name}'
        return ''


class CreateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'work', 'text', 'base_comment', 'reply_to']


class WorkSerializer(ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    likes = SerializerMethodField()
    is_liked = SerializerMethodField()
    comments_count = SerializerMethodField()

    class Meta:
        model = Work
        fields = ['id', 'name', 'student', 'author', 'teacher', 'issue', 'novelty',
                  'field', 'tasks', 'significance', 'tools', 'aprobation',
                  'keywords', 'status', 'comments', 'likes',
                  'is_liked', 'message', 'comments_count',
                  'tasks_category', 'field_category'] # TODO: message only for teacher review
        read_only_fields = ['message']

    def to_representation(self, instance):
        # print(instance)
        # instance.comments = instance.comments.filter(base_comment__isnull=True)
        data = super().to_representation(instance)
        if self.context['request'].method in SAFE_METHODS:
            data['student'] = PublicStudentSerializer(instance.student.user).data
            data['comments'] = CommentSerializer(instance.comments.filter(base_comment__isnull=True), many=True).data
        return data

    def get_likes(self, value):
        return value.liked_users.count()

    def get_is_liked(self, value):
        return bool(value.liked_users.filter(
            id=self.context['request'].user.id))

    def get_comments_count(self, value):
        return value.comments.count()


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
