from rest_framework import serializers
from rest_framework.decorators import action

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

