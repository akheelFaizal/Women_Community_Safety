from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from reports.models import Report

@staff_member_required
def admin_dashboard(request):
    # Analytics
    total_reports = Report.objects.count()
    status_counts = Report.objects.values('status').annotate(count=Count('status'))
    category_counts = Report.objects.values('category').annotate(count=Count('category'))
    
    # Simple logic for unsafe zones (group by location description loosely)
    # real production code would use geohashing or standardized locations
    location_counts = Report.objects.values('location_text').annotate(count=Count('location_text')).order_by('-count')[:5]
    
    context = {
        'total_reports': total_reports,
        'status_counts': status_counts,
        'category_counts': category_counts,
        'unsafe_zones': location_counts,
        'recent_reports': Report.objects.all().order_by('-created_at')[:10],
    }
    return render(request, 'admin_panel/dashboard.html', context)
