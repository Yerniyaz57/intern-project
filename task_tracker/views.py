from django.shortcuts import render
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .tasks import send_email_task
# Create your views here.

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [AllowAny, ]

class ChangeStatusViewSet(ModelViewSet):
    queryset = ChangeStatus.objects.all()
    serializer_class = ChangeStatusSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        import datetime as dt
        validated_data = request.data
        task = Task.objects.filter(pk=validated_data['task']).first()
        task.status = validated_data['next_status']
        task.save()
        print(task)
        print(task.supervisors)
        for i in task.supervisors.all():
            send_email_task()
        # return super().create(request, *args, **kwargs)

class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny, ]