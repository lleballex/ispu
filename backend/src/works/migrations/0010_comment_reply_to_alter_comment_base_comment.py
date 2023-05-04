# Generated by Django 4.1.6 on 2023-04-30 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0009_alter_work_field_category_alter_work_tasks_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='works.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='base_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='common_replies', to='works.comment'),
        ),
    ]