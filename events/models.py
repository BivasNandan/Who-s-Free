from django.db import models
import uuid
from django.conf import settings
# Create your models here.
class Event(models.Model):

    #basic information of An Event
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    EVENT_CATEGORY_CHOICES = [
        ('CONCERT', 'Concert'),
        ('WORKSHOP', 'Workshop'),
        ('SEMINAR', 'Seminar'),
        ('CONFERENCE', 'Conference'),
        ('MEETUP', 'Meetup'),
    ]
    category = models.CharField(max_length=15, choices=EVENT_CATEGORY_CHOICES)

    #time and date of the event
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    #location of the event
    location = models.TextField()

    #user/organizer information of the event
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    organizer_email = models.EmailField(max_length=255, blank=True, null=True)
    organizer_phone = models.CharField(max_length=15, blank=True, null=True)

    # Capacity and Attendance
    capacity = models.PositiveIntegerField()
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending_events', blank=True)
    is_free = models.BooleanField(default=True)

    # Media
    banner_image = models.ImageField(upload_to='event_banners/', blank=True, null=True)

    # Status and Visibility
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name