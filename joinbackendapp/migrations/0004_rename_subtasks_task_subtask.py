# Generated by Django 4.2.6 on 2023-10-14 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joinbackendapp', '0003_alter_task_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='subtasks',
            new_name='subtask',
        ),
    ]
