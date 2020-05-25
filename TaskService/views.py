from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from TaskService.models import Task, Log
from django.shortcuts import get_object_or_404
from TaskService.serializers import TaskSerializer, LogSerializer, CheckSerializer, WorkSerializer, CreateTaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from django.core.files.storage import default_storage
from django.db import transaction
import requests


def update_scheduled_task(data):
    pass

class ScheduledTaskView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TaskViewSetManager(viewsets.ModelViewSet):
    """
        ViewSet для CRUD операций над заданиями
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)




class ScheduledTask(APIView):

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskManager(APIView):
    """
        APIView для CRUD операции над заданиями (менеджер)
    """
    # Получить все задания
    def get(self, request):
        tasks = Task.objects.all()
        serializer = WorkSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # Создать задание
    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Редактировать задание. Если задание получает статус FILED, то переносится в Log
    @transaction.atomic
    def put(self, request):
        task = Task.objects.get_object_or_404(id=request.data['id'])
        if request.data['status'] == "FILED":
            log_serializer = LogSerializer(task)
            if log_serializer.is_valid():

                log_serializer.save()
                return Response(log_serializer.data, status=status.HTTP_200_OK)
            return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удалить задание
    def delete(self, request):
        Task.objects.get(id=request.data['id']).delete()
        return Response(status=status.HTTP_200_OK)

class TaskWorker(APIView):
    """
        APIView для CRUD операции над заданиями (рабочий)
    """
    # Получить все свои задания
    def get(self, request):
        tasks = Task.objects.filter(status='ISSUED', workers=request.data['worker'])
        serializer = WorkSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # Редактировать задание
    # TODO валидация
    def put(self, request):
        task = get_object_or_404(Task, id=request.data['id'])
        task.status = request.data['status']
        file = request.FILES['file']
        default_storage.save("home/reports/" + file.name, file)
        task.report = file.name
        # task.save()
        serializer = WorkSerializer(data=task)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogViewSetManager(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TaskViewWorker(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, ]

    # Рабочий отправил отчет
    # TODO при загрузке отчета статус не изменяется на completed
    def put(self, request):
        file = request.FILES['file']
        default_storage.save("home/reports/" + file.name, file)
        task = get_object_or_404(Task, id=request.data['id'])
        task.report = file.name
        task.save()
        return Response(status=status.HTTP_200_OK)

    # Отправить для рабочего все его задачи
    def get(self, request):
        work = Task.objects.filter(status='ISSUED', workers=request.data['worker'])
        serializer = WorkSerializer(work)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CheckPermissions(APIView):
    """
        Проверка прав по сгенерированному токену JWT
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        check = User.objects.get(id=request.user.id)
        serializer = CheckSerializer(check)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
