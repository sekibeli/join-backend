# Generated by Django 4.2.6 on 2023-10-21 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joinbackendapp', '0010_category_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='due_date',
            new_name='dueDate',
        ),
    ]
