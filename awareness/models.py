from django.db import models
from django.conf import settings

class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_alert = models.BooleanField(default=False, help_text="Urgent Safety Alert.")
    is_announcement = models.BooleanField(default=False, help_text="System-wide Announcement (Admin only).")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        label = "[ALERT]" if self.is_alert else "[A]" if self.is_announcement else ""
        return f"{label} {self.title} ({self.get_status_display()})"

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)
    priority = models.IntegerField(default=0, help_text="Higher number appears first")
    
    class Meta:
        ordering = ['-priority']
    
    def __str__(self):
        return self.name
