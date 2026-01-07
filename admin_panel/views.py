from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.contrib import messages
from reports.models import Report
from django.utils import timezone
from datetime import timedelta

def is_admin(user):
    return user.is_authenticated and (user.groups.filter(name='Admins').exists() or user.is_superuser)

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    # Standard Analytics
    total_reports = Report.objects.count()
    status_counts = Report.objects.values('status').annotate(count=Count('status'))
    category_counts = Report.objects.values('category').annotate(count=Count('category'))
    
    # Date Filtering (Weekly/Monthly)
    period = request.GET.get('period', 'all')
    reports_filtered = Report.objects.all()
    
    if period == 'week':
        start_date = timezone.now() - timedelta(days=7)
        reports_filtered = reports_filtered.filter(created_at__gte=start_date)
    elif period == 'month':
        start_date = timezone.now() - timedelta(days=30)
        reports_filtered = reports_filtered.filter(created_at__gte=start_date)
        
    unsafe_zones = reports_filtered.values('location_text').annotate(count=Count('location_text')).order_by('-count')[:5]

    context = {
        'total_reports': total_reports,
        'status_counts': status_counts,
        'category_counts': category_counts,
        'unsafe_zones': unsafe_zones,
        'recent_reports': Report.objects.all().order_by('-created_at')[:10],
        'period': period
    }
    return render(request, 'admin_panel/dashboard.html', context)

@user_passes_test(is_admin, login_url='login')
def user_management(request):
    users = User.objects.all().exclude(is_superuser=True)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(User, id=user_id)
        
        if action == 'disable':
            user.is_active = False
            user.save()
            messages.success(request, f'User {user.username} disabled.')
        elif action == 'enable':
            user.is_active = True
            user.save()
            messages.success(request, f'User {user.username} enabled.')
            
        return redirect('user_management')
        
    return render(request, 'admin_panel/users.html', {'users': users})

@user_passes_test(is_admin, login_url='login')
def report_management(request):
    reports = Report.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        action = request.POST.get('action')
        report = get_object_or_404(Report, id=report_id)
        
        if action == 'delete':
            report.delete()
            messages.success(request, 'Report deleted successfully.')
        elif action == 'override_status':
            new_status = request.POST.get('status')
            report.status = new_status
            report.save()
            messages.success(request, f'Status for Report #{report.id} updated to {report.get_status_display()}.')
            
        return redirect('report_management')
        
    return render(request, 'admin_panel/reports.html', {'reports': reports})
