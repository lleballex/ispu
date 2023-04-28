from . import views

from django.urls import path


urlpatterns = [
    path('', views.WorksView.as_view()),
    path('<int:pk>/', views.WorkView.as_view()),
    path('tasks-categories/', views.TasksCategoriesView.as_view()),
    path('field-categories/', views.FieldCategoriesView.as_view()),
]
