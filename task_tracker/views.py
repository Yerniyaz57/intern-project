from django.contrib.auth import login
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .tasks import send_email_task
# Create your views here.

class TaskViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication,]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def create(self, request, *args, **kwargs):
        validated_data = request.data
        if validated_data['planned_time']:
            user = User.objects.filter(id=validated_data['performer']).first()
            send_email_task.delay(user.email, 'Задача создана')
            send_email_task.apply_async(args=[user.email, 'Срок задачи истекло'], eta=validated_data['planned_time'])
        return super().create(request, *args, **kwargs)

class ChangeStatusViewSet(ModelViewSet):
    queryset = ChangeStatus.objects.all()
    serializer_class = ChangeStatusSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        validated_data = request.data
        task = Task.objects.filter(pk=validated_data['task']).first()
        task.status = validated_data['next_status']
        task.save()
        reminder = Reminder.objects.create(task=task, text="статус изменился")
        reminder.users.set(task.supervisors.all())
        for i in reminder.users.all():
            send_email_task.delay(i.email, reminder.text)
        return super().create(request, *args, **kwargs)

class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny, ]

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
