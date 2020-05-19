from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskStatus(Enum):
    REQUESTED = "REQUESTED"
    PLANNED = "PLANNED"
    ISSUED = "ISSUED"
    COMPLETED = "COMPLETED"
    CONTROLLED = "CONTROLLED"
    FILED = "FILED"
    DELETED = "DELETED"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class TaskType(Enum):
    SCHEDULED = "SCHEDULED"
    UNSCHEDULED = "UNSCHEDULED"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class UserPosition(Enum):
    MANAGER = "MANAGER"
    WORKER = "WORKER"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class Tasks(models.Model):
    creation_date = models.DateField()
    ending_date = models.DateField()
    status = models.CharField(max_length=255, choices=TaskStatus.choices())
    type = models.CharField(max_length=255, choices=TaskType.choices())
    description = models.TextField()
    report = models.CharField(max_length=100)
    link_to_object = models.CharField(max_length=100)
    link_to_component = models.CharField(max_length=100)

    class Meta:
        ordering = ('creation_date',)

    def __str__(self):
        return self.description


class User(AbstractUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position = models.CharField(max_length=255, choices=UserPosition.choices())


class WorkersTasks(models.Model):
    id_U = models.ForeignKey(User, on_delete=models.CASCADE)
    id_T = models.ForeignKey(Tasks, on_delete=models.CASCADE)
