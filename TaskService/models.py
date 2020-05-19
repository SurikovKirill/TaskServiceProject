from django.db import models
from django.contrib.auth.models import AbstractUser


class Tasks(models.Model):
    STATUS_CHOICES = ('requested', 'planned', 'issued', 'completed', 'controlled', 'filed', 'deleted')
    TYPE_CHOICES = ('scheduled', 'unscheduled')
    creation_date = models.DateField()
    ending_date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES)
    type = models.CharField(choices=TYPE_CHOICES)
    description = models.CharField()
    report = models.CharField()
    link_to_object = models.CharField()
    link_to_component = models.CharField()

    class Meta:
        ordering = ('creation_date',)

    def __str__(self):
        return self.description


class User(AbstractUser):
    POSITION_CHOICES = ('manager', 'worker')
    name = models.CharField()
    surname = models.CharField()
    position = models.CharField(choices=POSITION_CHOICES)


class WorkersTasks(models.Model):
    id_U = models.ForeignKey(User, on_delete=models.CASCADE)
    id_T = models.ForeignKey(Tasks, on_delete=models.CASCADE)
