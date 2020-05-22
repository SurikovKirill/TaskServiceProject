from rest_framework import serializers
from TaskService.models import User, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'creation_date', 'ending_date', 'status', 'task_type', 'description', 'report',
                  'link_to_object', 'link_to_component']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
