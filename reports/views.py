from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report, ReportAttachment
from .forms import ReportForm

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            
            # Handle attachment
            attachment = form.cleaned_data.get('attachment')
            if attachment:
                ReportAttachment.objects.create(report=report, file=attachment)
                
            messages.success(request, 'Report submitted successfully. We will review it shortly.')
            return redirect('user_dashboard')
    else:
        form = ReportForm()
    return render(request, 'reports/report_form.html', {'form': form})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    # Ensure user can only see their own reports unless moderator
    if report.user != request.user and not request.user.is_moderator:
        messages.error(request, "You do not have permission to view this report.")
        return redirect('user_dashboard')
        
    return render(request, 'reports/report_detail.html', {'report': report})

@login_required
def report_list(request):
    reports = Report.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})
