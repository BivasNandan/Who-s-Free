from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings

class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Common fields
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=True)
    birth_date = models.DateField(null=True, blank=False)#only for individuals
    bio = models.CharField(max_length=255, blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)

    # Fields specific to businesses
    company_name = models.CharField(max_length=255, blank=False, null=True)
    business_address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    sector = models.CharField(max_length=255, null=True, blank=True) #in which sector the company operates

    # Fields specific to individuals
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)

    is_profile_complete = models.BooleanField(default=False) # New field to track profile completion

    def __str__(self):
        return f"{self.username} {self.user_type}"
    
    def friends(self):
        """Return a list of accepted friends."""
        sent = Friendship.objects.filter(from_user=self, status='accepted').values_list('to_user', flat=True)
        received = Friendship.objects.filter(to_user=self, status='accepted').values_list('from_user', flat=True)
        return CustomUser.objects.filter(id__in=list(sent) + list(received))

    def friend_requests(self):
        """Return a list of pending friend requests received."""
        return Friendship.objects.filter(to_user=self, status='pending')

    def sent_friend_requests(self):
        """Return a list of pending friend requests sent."""
        return Friendship.objects.filter(from_user=self, status='pending')
    
class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friend_requests_sent',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friend_requests_received',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # Prevent duplicate friend requests

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"