from .models import User, StudentProfile, TeacherProfile

from django.contrib import admin


admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
