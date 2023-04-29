from .models import Work, TasksCategory, FieldCategory, Comment
from .serializers import CommentSerializer, TasksCategorySerializer, FieldCategorySerializer, UpdateWorkSerializer, \
                         WorkSerializer, WorkListSerializer, \
                         CreateCommentSerializer, ReviewWorkSerializer

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
                                  RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class TasksCategoriesView(ListModelMixin, GenericAPIView):
    queryset = TasksCategory.objects.all()
    serializer_class = TasksCategorySerializer

    def get(self, request):
        return self.list(request)


class FieldCategoriesView(ListModelMixin, GenericAPIView):
    queryset = FieldCategory.objects.all()
    serializer_class = FieldCategorySerializer 

    def get(self, request):
        return self.list(request)


class WorksView(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]   # TODO: only students

    def get(self, request):
        return self.list(request)

    def post(self, request):
        request.data['student'] = request.user.student_profile.id
        return self.create(request)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return WorkListSerializer
        return WorkSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        tasks_categories = self.request.query_params.get('tasks_categories')
        field_categories = self.request.query_params.get('field_categories')

        print(query, tasks_categories, field_categories)

        works = Work.objects.filter(status='ACCEPTED', name__icontains=query)

        if (tasks_categories):
            works = works.filter(
                tasks_category__in=tasks_categories.split(', '))

        if (field_categories):
            works = works.filter(
                field_category__in=field_categories.split(', '))

        return works


class WorkView(RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    # queryset = Work.objects.filter(status='ACCEPTED')
    serializer_class = WorkSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        query = Q(status='ACCEPTED')

        if self.request.user.is_authenticated:
            if self.request.user.teacher_profile:
                query.add(Q(teacher=self.request.user.teacher_profile.id), Q.OR)

            if self.request.user.student_profile:
                query.add(Q(student=self.request.user.student_profile.id), Q.OR)

        return Work.objects.filter(query)


class UpdateWorkView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UpdateWorkSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_queryset(self):
        return Work.objects.filter(
            student=self.request.user.student_profile.id)

class SendCommentView(CreateModelMixin, GenericAPIView):
    serializer_class = CreateCommentSerializer
    # serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def post(self, request):
        request.data.update(user=request.user.id)
        return self.create(request)


class ToggleLikeView(GenericAPIView):
    queryset = Work.objects.filter(status='ACCEPTED')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        instance = self.get_object()

        if instance.liked_users.filter(id=request.user.id):
            instance.liked_users.remove(request.user)
        else:
            instance.liked_users.add(request.user)

        instance.save()

        return Response({
            'likes': instance.liked_users.count(),
            'is_liked': bool(instance.liked_users.filter(id=request.user.id)),
        })


class ReviewWorkView(UpdateModelMixin, GenericAPIView):
    queryset = Work.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # TODO: permission and queryset - only for teachers and pernding status?
    serializer_class = ReviewWorkSerializer

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteCommentView(DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user.id)
