from django.db import models
from django.conf import settings

class Report(models.Model):
    CATEGORY_CHOICES = [
        ('harassment', 'Harassment'),
        ('domestic_violence', 'Domestic Violence'),
        ('unsafe_area', 'Unsafe Zone'),
        ('suspicious_activity', 'Suspicious Activity'),
        ('emergency', 'Emergency/SOS'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('responded', 'Responded'),
        ('escalated', 'Escalated'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    # User is optional for anonymous reports, or if we want to track who submitted it even if 'is_anonymous' is True
    # The requirement says: "if anonymous, hide identity from moderators". So we can still link it to user but hide it in views.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location_text = models.CharField(max_length=255, help_text="e.g., Near City Center Bus Stop")
    
    # Optional Lat/Lng for map
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_anonymous = models.BooleanField(default=False, help_text="If checked, your identity will be hidden from moderators.")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class ReportAttachment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='report_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for Report #{self.report.id}"
