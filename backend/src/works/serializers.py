from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Work, TasksCategory, FieldCategory
from users.serializers import PublicTeacherSerializer



class TasksCategorySerializer(ModelSerializer):
    class Meta:
        model = TasksCategory
        fields = ['id', 'name']


class FieldCategorySerializer (ModelSerializer):
    class Meta:
        model = FieldCategory 
        fields = ['id', 'name']


class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'name', 'student', 'teacher', 'issue', 'novelty',
                  'field', 'tasks', 'significance', 'tools', 'aprobation',
                  'keywords', 'status']

class WorkListSerializer(ModelSerializer):
    tasks_category = TasksCategorySerializer()
    field_category = FieldCategorySerializer()

    
    class Meta:
        model = Work
        fields = ['id', 'name', 'issue', 'tasks_category', 'field_category']


class UserWorkListSerializer(ModelSerializer):
    teacher = PublicTeacherSerializer(source='teacher.user')

    class Meta:
        model = Work
        fields = ['id', 'name', 'teacher', 'status']


