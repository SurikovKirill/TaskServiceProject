from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from TaskService.models import Task
from TaskService.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from django.core.files.storage import default_storage


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class TaskView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,]

    def put(self, request):
        file = request.FILES['file']
        path = default_storage.save("home/reports/"+file.name, file)
        # file_obj = request.data['file']
        print(request.data)
        return Response(status=204)



#
# class TasksViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = (permissions.IsAuthenticated,)
