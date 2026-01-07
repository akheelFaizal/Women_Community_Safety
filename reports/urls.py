from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.create_report, name='create_report'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('my-reports/', views.report_list, name='report_list'),
]
