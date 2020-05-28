from rest_framework import serializers
from TaskService.models import User, Task, Log, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class TaskSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'creation_date', 'ending_date', 'status', 'task_type', 'description', 'report',
                  'object_data', 'components', 'worker']

class CreateTaskSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id','creation_date', 'ending_date', 'status', 'task_type', 'description',
                  'object_data', 'components', 'worker']


class WorkSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'creation_date', 'ending_date', 'status', 'task_type', 'description', 'report', 'object_data',
                  'components', 'worker']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'groups']
