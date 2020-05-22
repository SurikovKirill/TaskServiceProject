from enum import Enum
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


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


class Task(models.Model):
    creation_date = models.DateField()
    ending_date = models.DateField()
    status = models.CharField(max_length=255, choices=TaskStatus.choices())
    task_type = models.CharField(max_length=255, choices=TaskType.choices())
    description = models.TextField()
    report = models.CharField(max_length=100)
    link_to_object = models.CharField(max_length=100)
    link_to_component = models.CharField(max_length=100)
    workers = models.ManyToManyField(User)

    class Meta:
        ordering = ('creation_date',)

    def __str__(self):
        return self.description


class Log(models.Model):
    creation_date = models.DateField()
    ending_date = models.DateField()
    task_type = models.CharField(max_length=255, choices=TaskType.choices())
    description = models.TextField()
    report = models.CharField(max_length=100)
    link_to_object = models.CharField(max_length=100)
    link_to_component = models.CharField(max_length=100)
    user = JSONField()

    class Meta:
        ordering = ('-ending_date',)