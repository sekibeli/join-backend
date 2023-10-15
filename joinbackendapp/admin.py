from django.contrib import admin
from .models import Category, Contact, Priority, Status, Subtask, Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    filter_horizontal = ('assigned',)
    
# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Contact)
