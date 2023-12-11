from django.urls import path, include
from rest_framework import routers
from .views import AssignedView, CreateTaskWithSubtasks, SignupView, SubtaskView, TaskSearchView, TaskView, CategoryView, ContactView, LoginView, UserView
#from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'tasks', TaskView, basename="TaskViewRoute")
router.register(r'categories', CategoryView, basename="CategoryViewRoute")
router.register(r'contacts', ContactView, basename="ContactViewRoute")
router.register(r'subtasks', SubtaskView, basename="SubtaskViewRoute")
router.register(r'assigned', AssignedView, basename="AssignedViewRoute")


urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("signup/", SignupView.as_view(), name='signup'),
    path("user/", UserView.as_view(), name='current_user'),
    path("create_task_with_subtasks/", CreateTaskWithSubtasks.as_view(), name='create_task_with_subtasks'),
    path('subtasks/update_many/', SubtaskView.as_view({'put': 'update_many'})),
    path('tasks/<int:pk>/add_subtasks/', SubtaskView.as_view({'post': 'add_subtasks'})),
    path('search/', TaskSearchView.as_view(), name='task-search'),
    path("", include(router.urls))
]