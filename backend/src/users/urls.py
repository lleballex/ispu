from . import views

from django.urls import path


urlpatterns = [
    path('', views.RegisterUserView.as_view()),
    path('login/', views.LoginView.as_view()),
]
