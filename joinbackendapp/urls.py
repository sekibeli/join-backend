from django.urls import path, include
from rest_framework import routers
from .views import CreateTaskWithSubtasks, TaskView, CategoryView, ContactView, LoginView
#from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'tasks', TaskView, basename="TaskViewRoute")
router.register(r'categories', CategoryView, basename="CategoryViewRoute")
router.register(r'contacts', ContactView, basename="ContactViewRoute")


urlpatterns = [
    # path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(), name='login'),
    path("create_task_with_subtasks/", CreateTaskWithSubtasks.as_view(), name='create_task_with_subtasks'),
    path("", include(router.urls))
]