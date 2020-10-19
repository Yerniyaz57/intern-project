from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, ChangeStatusViewSet, ReminderViewSet, LoginView

router = routers.DefaultRouter(trailing_slash=False)
router.register('tasks', TaskViewSet, basename='tasks')
router.register('task/status', ChangeStatusViewSet, basename='change_status')
router.register('reminder', ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
]
