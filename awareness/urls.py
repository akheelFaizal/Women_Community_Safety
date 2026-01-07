from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.awareness_feed, name='awareness_feed'),
    path('emergency/', views.emergency_contacts, name='emergency_contacts'),
    path('emergency/add/', views.add_emergency_contact, name='add_emergency_contact'),
    path('emergency/edit/<int:pk>/', views.edit_emergency_contact, name='edit_emergency_contact'),
    path('emergency/delete/<int:pk>/', views.delete_emergency_contact, name='delete_emergency_contact'),
]
