from users.models import User, StudentProfile, TeacherProfile

from django.db import models
from django.contrib.postgres.fields import ArrayField


WORK_STATUSES = [
    ('PENDING', 'On verification'),
    ('ACCEPTED', 'Accepted'),
    ('REJECTED', 'Rejected'),
]


class TasksCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FieldCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=255)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,
                                related_name='works')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE,
                                related_name='works')
    issue = models.CharField(max_length=255)
    novelty = models.TextField()
    field = models.CharField(max_length=255)
    tasks = models.TextField()
    significance = models.TextField()
    tools = models.TextField()
    aprobation = models.CharField(max_length=255)
    keywords = ArrayField(models.CharField(max_length=30), blank=True)

    # related_works from db
    # related_works from link

    tasks_category = models.ForeignKey(TasksCategory, related_name='works',
                                       on_delete=models.CASCADE, blank=True,
                                       null=True)
    field_category = models.ForeignKey(FieldCategory, related_name='works',
                                       on_delete=models.CASCADE, blank=True,
                                       null=True)

    status = models.CharField(max_length=30, choices=WORK_STATUSES, default='PENDING')
    # message = models.TextField()



class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments',
                             on_delete=models.CASCADE)
    text = models.TextField()
    work = models.ForeignKey(Work, on_delete=models.CASCADE,
                             related_name='comments')
