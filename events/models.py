from django.db import models
from django.conf import settings
import uuid

class Event(models.Model):
    # Basic information of an event
    banner = models.ImageField(upload_to='banner/', blank=True, null=True)
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    EVENT_CATEGORY_CHOICES = [
        ('CONCERT', 'Concert'),
        ('WORKSHOP', 'Workshop'),
        ('SEMINAR', 'Seminar'),
        ('CONFERENCE', 'Conference'),
        ('MEETUP', 'Meetup'),
    ]
    category = models.CharField(max_length=15, choices=EVENT_CATEGORY_CHOICES)

    # Time and date of the event
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Location of the event
    location = models.CharField(max_length=255)

    # User/organizer information of the event
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')

    # Users interested in the event
    interested_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interested_events', blank=True)

    def __str__(self):
        return self.name