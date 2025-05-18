# notifications/urls.py

from django.urls import path
from .views import mes_notifications

urlpatterns = [
    path('', mes_notifications, name='mes_notifications'),
]
