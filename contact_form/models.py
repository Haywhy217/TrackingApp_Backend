from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Ensure this field is included

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
