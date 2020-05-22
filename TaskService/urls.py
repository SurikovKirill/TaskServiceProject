from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tasks', views.TasksViewSet)
# router.register(r'users', views.UserViewSet)
# router.register(r'saverep', views.TaskView)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'task/', views.TaskViewWorker.as_view())
]