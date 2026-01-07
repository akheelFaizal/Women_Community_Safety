from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Post, EmergencyContact
from .forms import EmergencyContactForm

def is_admin(user):
    return user.is_authenticated and (user.groups.filter(name='Admins').exists() or user.is_superuser)

def awareness_feed(request):
    alerts = Post.objects.filter(is_alert=True, status='published').order_by('-created_at')
    posts = Post.objects.filter(is_alert=False, status='published').order_by('-created_at')
    return render(request, 'awareness/feed.html', {'alerts': alerts, 'posts': posts})

def emergency_contacts(request):
    contacts = EmergencyContact.objects.all()
    return render(request, 'awareness/emergency.html', {'contacts': contacts})

@user_passes_test(is_admin, login_url='login')
def add_emergency_contact(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emergency contact added successfully.')
            return redirect('emergency_contacts')
    else:
        form = EmergencyContactForm()
    return render(request, 'awareness/emergency_form.html', {'form': form, 'action': 'Add'})

@user_passes_test(is_admin, login_url='login')
def edit_emergency_contact(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emergency contact updated successfully.')
            return redirect('emergency_contacts')
    else:
        form = EmergencyContactForm(instance=contact)
    return render(request, 'awareness/emergency_form.html', {'form': form, 'action': 'Edit'})

@user_passes_test(is_admin, login_url='login')
def delete_emergency_contact(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk)
    contact.delete()
    messages.success(request, 'Emergency contact deleted.')
    return redirect('emergency_contacts')
