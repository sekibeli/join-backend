# Generated by Django 4.2.6 on 2023-10-15 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joinbackendapp', '0006_remove_task_subtask_subtask_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='joinbackendapp.task'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='assigned',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned',
            field=models.ManyToManyField(blank=True, null=True, related_name='tasks', to='joinbackendapp.contact'),
        ),
    ]