from rest_framework import serializers
from TaskService.models import User, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class TaskSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'creation_date', 'ending_date', 'status', 'task_type', 'description', 'report',
                  'link_to_object', 'link_to_component', 'workers']
