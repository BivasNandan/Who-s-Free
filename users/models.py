from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

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
    bio = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    # Fields specific to businesses
    company_name = models.CharField(max_length=255, blank=False, null=True)
    business_address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    sector = models.CharField(max_length=255, null=True, blank=True) #in which sector the company operates

    # Fields specific to individuals
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)

    is_profile_complete = models.BooleanField(default=False) # New field to track profile completion

    def __str__(self):
        return f"{self.username} {self.user_type}"