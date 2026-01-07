from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_analytics'),
    path('users/', views.user_management, name='user_management'),
    path('reports/', views.report_management, name='report_management'),
]
