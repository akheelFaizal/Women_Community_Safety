from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib import messages
from reports.models import Report

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('user_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_dashboard(request):
    # Check if user is in Moderators or Admins group
    if request.user.groups.filter(name__in=['Moderators', 'Admins']).exists() or request.user.is_superuser:
        return redirect('moderator_dashboard')
    
    # We will fetch reports here later
    reports = Report.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'reports': reports 
    }
    return render(request, 'accounts/dashboard.html', context)
