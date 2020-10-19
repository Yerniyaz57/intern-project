from django.contrib.auth import authenticate
from django.core import exceptions
from rest_framework import serializers

from .models import Task, ChangeStatus, Reminder, User

class PerformerForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return User.objects.filter(is_performer=True)

class SupervisorsForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return User.objects.filter(is_supervisor=True)

class TaskCreateSerializer(serializers.ModelSerializer):
    performer = PerformerForeignKey()
    supervisors = SupervisorsForeignKey(many=True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'performer', 'supervisors', 'status', 'time_begin', 'time_end', 'planned_time')



class ChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeStatus
        fields = ('id', 'prev_status', 'next_status', 'task', 'performer')

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ('id', 'task', 'text', 'users')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated. "
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials. "
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both. "
            raise exceptions.ValidationError(msg)
        return data


