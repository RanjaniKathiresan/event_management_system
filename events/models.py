from django.db import models

# Create your models here.
class Events(models.Model):
    event_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Attendee(models.Model):
    event = models.ForeignKey(Events, related_name='attendees', on_delete=models.CASCADE)
    attentee_name =models.CharField(max_length=100)
    email_id = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'email_id'], name='unique_event_email')
        ]
