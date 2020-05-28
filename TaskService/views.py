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
from django.db.models import Q
from django.db import transaction
import requests
import json
import time
import datetime

# TODO реализовать, протестировать
# Запрос часов наработки
def get_operating_hours(id):
    url = 'http://127.0.0.1:8002/api/component/'+str(id)
    req=requests.get(url)
    data = req.json()
    return data['operating_hours']



class ScheduledTaskView(APIView):
    permission_classes = [AllowAny]

    # Обработка запроса сервиса чертежей на добавление новой плановой задачи
    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO реализовать, протестировать
    def delete(self, request):
        print(request.data['id'])
        print(request.data['descendants'])
        try:
            Task.objects.filter(components__id=int(request.data['id'])).delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for item in request.data['descendants']:
            Task.objects.filter(components__id=int(item['id'])).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ScheduledTaskObject(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        try:
            Task.objects.filter(object_data__id=int(request.data['id'])).delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for item in request.data['descendants']:
            Task.objects.filter(components__id=int(item['id'])).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    # TODO протестировать, реализовать запрос на сервис чертежей, реализовать функцию пересчета по часам наработки
    # Редактировать задание
    # @transaction.atomic
    def put(self, request):
        try:
            id_ = request.data['id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Поиск задания
        task = Task.objects.get_object_or_404(id=id_)
        # Если задание приобретает статус FILED, то
            # Если задание внеплановое, то берем компонент в задании и ищем по компоненту плановую задачу
                # Если есть плановая задача на компонент, то отправляем запрос к сервису чертежей, чтобы узнать часы наработки
                # Сохраняем задачу в архиве, удаляем из таблицы, для найденной плановой редактируем creation_date с учетом полученных часов наработки
            # Если задание плановое, то сохраняем в архив, меняем статус задания, удаляем ссылку на репорт
        if request.data['status'] == "FILED":
            if task.task_type == "UNSCHEDULED":
                component = task.components['id']
                sch_task = Task.objects.get(components__id=component)
                operating_hours = get_operating_hours(component)
                log_serializer = LogSerializer(task)
                if log_serializer.is_valid():
                    log_serializer.save()
                    task.delete()
                sch_task.creation_date = sch_task.creation_date+datetime.timedelta(days=operating_hours)
            if task.task_type == "SCHEDULED":
                log_serializer = LogSerializer(task)
                if log_serializer.is_valid():
                    log_serializer.save()
                task.status = "PLANNED"
                operating_hours = get_operating_hours(task.components__id)
                task.creation_date = task.creation_date + datetime.timedelta(days=operating_hours)
                task.report = None
                task.save()


        log_serializer = LogSerializer(task)
        if log_serializer.is_valid():
            log_serializer.save()
            task.delete()
            return Response(log_serializer.data, status=status.HTTP_200_OK)
        return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Менеджер удалил задание (удаляются только внеплановые)
    def delete(self, request):
        try:
            id_ = request.data['id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            Task.objects.get(id=id_).delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

# TODO протестировать
# Работа с архивом
class LogViewSetManager(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TaskWorker(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, JSONParser]

    # TODO Протестировать
    # Рабочий обновил задачу
    def put(self, request):
        try:
            id_ = request.data['id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        task = get_object_or_404(Task, id=id_)
        try:
            status_ = request.data['status']
        except:
            status_ = task.status
        try:
            file = request.FILES['file']
            timestamp = str(int(time.time()))
            filename = timestamp + '_' + file.name
            default_storage.save(name=filename, content=file)
            default_storage.delete(task.report)
        except:
            filename = task.report
        task.report = filename
        task.status = status_
        task.save()
        return Response(status=status.HTTP_200_OK)

    # Отправить для рабочего все его задачи, пока работает только с form-data
    def get(self, request):
        try:
            worker = request.data['worker']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        work = Task.objects.filter(Q(status='ISSUED') & Q(worker__id=worker))
        serializer = WorkSerializer(work, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CheckPermissions(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Проверка прав по JWT токену
    def get(self, request):
        check = User.objects.get(id=request.user.id)
        serializer = CheckSerializer(check)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
