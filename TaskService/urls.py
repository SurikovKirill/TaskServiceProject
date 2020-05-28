from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'logs', views.LogViewSetManager)
# router.register(r'users', views.UserViewSet)
# router.register(r'saverep', views.TaskView)

urlpatterns = [
    path(r'api/log', include(router.urls)),
    path(r'api/permissions', views.CheckPermissions.as_view()), #
    path(r'api/tasks/manager', views.TaskManager.as_view()),#
    path(r'api/tasks/worker', views.TaskWorker.as_view()), #
    path(r'api/tasks/scheduled', views.ScheduledTaskView.as_view()),
    path(r'api/tasks/scheduled/object', views.ScheduledTaskObject.as_view())
]