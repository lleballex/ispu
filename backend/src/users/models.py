from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class StudentProfile(models.Model):
    number = models.IntegerField(unique=True)
    course = models.IntegerField()
    group = models.CharField(max_length=10)
    

class TeacherProfile(models.Model):
    pass


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_profile = models.OneToOneField(StudentProfile, blank=True,
                                           null=True, on_delete=models.CASCADE)
    teacher_profile = models.OneToOneField(TeacherProfile, blank=True,
                                           on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()


class Achievement(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,
                                related_name='achievements')

    is_approved = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    message = models.TextField(null=True)
