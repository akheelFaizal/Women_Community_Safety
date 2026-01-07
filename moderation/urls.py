from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.moderator_dashboard, name='moderator_dashboard'),
    path('review/<int:pk>/', views.review_report, name='review_report'),
    path('create-post/', views.create_awareness_post, name='create_post'),
]
