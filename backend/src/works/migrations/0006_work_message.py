# Generated by Django 4.1.6 on 2023-04-29 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0005_work_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='message',
            field=models.TextField(blank=True),
        ),
    ]
