from django.db import models
from django.contrib.auth.models import AbstractUser, Group
import hashlib

# Create your models here.


class user_details(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=False)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Add age field
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=[]

    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups", blank=True
    )

    user_permissions = models.ManyToManyField(
        Group, related_name="custom_user_permissions", blank=True
    )
    
class Address(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="House or Company Name")
    postoffice = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)

    def _str_(self):
        return self.name
