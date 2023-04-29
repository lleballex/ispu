from . import views

from django.urls import path


urlpatterns = [
    path('', views.WorksView.as_view()),
    path('<int:pk>/', views.WorkView.as_view()),
    path('<int:pk>/like/', views.ToggleLikeView.as_view()),
    path('<int:pk>/review/', views.ReviewWorkView.as_view()),
    path('<int:pk>/update/', views.UpdateWorkView.as_view()),
    path('comment/', views.SendCommentView.as_view()),
    path('comments/<int:pk>/', views.DeleteCommentView.as_view()),
    path('tasks-categories/', views.TasksCategoriesView.as_view()),
    path('field-categories/', views.FieldCategoriesView.as_view()),
]
