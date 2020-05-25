from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tasks', views.TaskViewSetManager)
router.register(r'logs', views.LogViewSetManager)
# router.register(r'users', views.UserViewSet)
# router.register(r'saverep', views.TaskView)

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path(r'task/<int:pk>/', views.TaskViewWorker.as_view()),
    path(r'api/v1/check', views.CheckPermissions.as_view()),
    path(r'api/tasks/manager', views.TaskManager.as_view()),
    path(r'api/tasks/worker', views.TaskWorker.as_view())
    # path(r'api/v2/tasks/worker', )
]