from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class user(models.Model):
    username=models.CharField(max_length=150,unique=True)
    email=models.EmailField(max_length=254,unique=True)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=15)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    date_join=models.DateTimeField(auto_now_add=True)

class user_profile(models.Model):
    usern = models.OneToOneField( user,on_delete=models.CASCADE   )          
    full_name=models.CharField(max_length=255)
    profile_image = models.ImageField(
    upload_to="profiles/",
    blank=True,
    null=True
)
    gender=models.CharField(max_length=10)
    dob=models.DateField()
    bio=models.TextField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
