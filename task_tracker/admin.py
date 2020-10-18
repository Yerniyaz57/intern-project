from django.contrib import admin
from .models import User, Task, ChangeStatus, Reminder
# Register your models here.

admin.site.register(User)
admin.site.register(Task)
admin.site.register(ChangeStatus)
admin.site.register(Reminder)