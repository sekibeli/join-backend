from django.urls import path, include
from rest_framework import routers
from .views import TaskView
from django.contrib import admin

router = routers.DefaultRouter()
router.register("tasks", TaskView, basename="TaskViewRoute")

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", include(router.urls))
]