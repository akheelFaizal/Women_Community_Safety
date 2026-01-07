from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib import messages
from reports.models import Report
from .forms import ReportResponseForm, PostForm

def is_moderator(user):
    return user.is_authenticated and (user.groups.filter(name='Moderators').exists() or user.is_superuser)

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
    
    # Handle response form
    if request.method == 'POST' and 'response_submit' in request.POST:
        response_form = ReportResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.report = report
            response.responder = request.user
            response.save()
            
            # Auto-update status if it was submitted
            if report.status == 'submitted':
                report.status = 'under_review'
                report.save()
                
            messages.success(request, 'Response added successfully.')
            return redirect('review_report', pk=pk)
    else:
        response_form = ReportResponseForm()

    # Handle status actions
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        
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
        
    return render(request, 'moderation/review_report.html', {
        'report': report,
        'response_form': response_form
    })

@permission_required('awareness.add_post', login_url='login')
def create_awareness_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Safety tip published successfully.')
            return redirect('moderator_dashboard')
    else:
        form = PostForm()
    return render(request, 'moderation/create_post.html', {'form': form})
