from .models import Work, TasksCategory, FieldCategory, Comment

from django.contrib import admin


admin.site.register(Work)
admin.site.register(TasksCategory)
admin.site.register(FieldCategory)
admin.site.register(Comment)
