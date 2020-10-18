from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class User(AbstractUser):
    is_performer = models.BooleanField(default=0, null=True)
    is_supervisor = models.BooleanField(default=0, null=True)

    def __str__(self):
        return self.username

class Task(models.Model):
    MATCH_PLANNED = 0
    MATCH_ACTIVE = 1
    MATCH_CONTROL = 2
    MATCH_COMPLETED = 3
    STATUS_CHOICES = (
        (MATCH_PLANNED, _('Планируется')),
        (MATCH_ACTIVE, _('Активная')),
        (MATCH_CONTROL, _('Контроль')),
        (MATCH_COMPLETED, _('Завершена')),
    )
    title = models.CharField(max_length=255, blank=True, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='my_tasks', verbose_name='исполнитель')
    supervisors = models.ManyToManyField(User, related_name="tasks", verbose_name='наблюдатели')
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        verbose_name='статус'
    )
    time_begin = models.DateTimeField(null=True, verbose_name='время начала')
    time_end = models.DateTimeField(null=True, verbose_name='время завершения')
    planned_time = models.DateTimeField(null=True, verbose_name='планируемое время завершения')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class ChangeStatus(models.Model):
    MATCH_PLANNED = 0
    MATCH_ACTIVE = 1
    MATCH_CONTROL = 2
    MATCH_COMPLETED = 3
    STATUS_CHOICES = (
        (MATCH_PLANNED, _('Планируется')),
        (MATCH_ACTIVE, _('Активная')),
        (MATCH_CONTROL, _('Контроль')),
        (MATCH_COMPLETED, _('Завершена')),
    )
    prev_status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='предыдущий статус')
    next_status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='следующий статус')
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name='change_status', verbose_name='задача')
    performer = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, related_name="change_status", verbose_name='кем изменен')

    class Meta:
        verbose_name = 'Изменение статуса'

class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name='reminders', verbose_name='задача')
    text = models.TextField(verbose_name='текст напоминания')
    users = models.ManyToManyField(User, related_name="reminders", verbose_name='пользователей')

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'