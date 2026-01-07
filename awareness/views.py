from django.shortcuts import render
from .models import Post, EmergencyContact

def awareness_feed(request):
    alerts = Post.objects.filter(is_alert=True).order_by('-created_at')
    posts = Post.objects.filter(is_alert=False).order_by('-created_at')
    return render(request, 'awareness/feed.html', {'alerts': alerts, 'posts': posts})

def emergency_contacts(request):
    contacts = EmergencyContact.objects.all()
    return render(request, 'awareness/emergency.html', {'contacts': contacts})
