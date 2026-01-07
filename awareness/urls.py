from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.awareness_feed, name='awareness_feed'),
    path('emergency/', views.emergency_contacts, name='emergency_contacts'),
]
