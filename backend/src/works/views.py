from .models import Work, TasksCategory, FieldCategory
from .serializers import TasksCategorySerializer, FieldCategorySerializer, \
                         WorkSerializer, WorkListSerializer

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
                                  RetrieveModelMixin


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
    queryset = Work.objects.filter(status='ACCEPTED')

    def get(self, request):
        return self.list(request)

    def post(self, request):
        request.data['student'] = request.user.student_profile.id
        return self.create(request)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return WorkListSerializer
        return WorkSerializer


class WorkView(RetrieveModelMixin, GenericAPIView):
    queryset = Work.objects.filter(status='ACCEPTED')
    serializer_class = WorkSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
