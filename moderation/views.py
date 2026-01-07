from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from reports.models import Report

def is_moderator(user):
    return user.is_authenticated and (user.is_moderator or user.is_superuser)

@user_passes_test(is_moderator, login_url='login')
def moderator_dashboard(request):
    # Fetch all reports, newest first
    reports = Report.objects.all().order_by('-created_at')
    
    context = {
        'reports': reports,
        'submitted_count': reports.filter(status='submitted').count(),
        'under_review_count': reports.filter(status='under_review').count(),
        'resolved_count': reports.filter(status='resolved').count(),
    }
    return render(request, 'moderation/dashboard.html', context)

@user_passes_test(is_moderator, login_url='login')
def review_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        
        if action == 'mark_under_review':
            report.status = 'under_review'
            messages.info(request, f'Report #{report.id} marked as Under Review.')
        elif action == 'resolve':
            report.status = 'resolved'
            messages.success(request, f'Report #{report.id} marked as Resolved.')
        elif action == 'escalate':
            report.status = 'escalated'
            messages.warning(request, f'Report #{report.id} escalated to Admin.')
            
        report.save()
        return redirect('moderator_dashboard')
        
    return render(request, 'moderation/review_report.html', {'report': report})
