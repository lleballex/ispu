from . import views

from django.urls import path


urlpatterns = [
    path('', views.RegisterUserView.as_view()),
    path('login/', views.LoginView.as_view()),
    
    path('teachers/', views.TeachersView.as_view()),

    path('works/', views.UserWorksView.as_view()),
]
