from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self.create_user(username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)

    # student_profile = models.OneToOneField(StudentProfile, blank=True,
                                           # null=True, on_delete=models.CASCADE)
    # teacher_profile = models.OneToOneField(TeacherProfile, blank=True,
                                           # on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    temp_password = models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = UserManager()


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='student_profile')
    number = models.IntegerField(unique=True)
    course = models.IntegerField()
    group = models.CharField(max_length=10)

    def __str__(self):
        return (f'{self.user.last_name} {self.user.first_name} '
                f'{self.user.patronymic}')


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='teacher_profile')

    def __str__(self):
        return (f'{self.user.last_name} {self.user.first_name} '
                f'{self.user.patronymic}')
