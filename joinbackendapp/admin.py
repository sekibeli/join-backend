from django.contrib import admin
from .models import Category, Contact, Priority, Status, Subtask, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Contact)
