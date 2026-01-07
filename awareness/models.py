from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_alert = models.BooleanField(default=False, help_text="Check if this is an urgent safety alert.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)
    priority = models.IntegerField(default=0, help_text="Higher number appears first")
    
    class Meta:
        ordering = ['-priority']
    
    def __str__(self):
        return self.name
