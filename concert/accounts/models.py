from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    ProfileImage = models.ImageField(upload_to="profileImages/", blank=True, null=True)

    Man = 1
    Woman = 2
    status_choices = ((Man,"مرد"),(Woman,"زن"))
    Gender = models.IntegerField(choices=status_choices, default=Man)
    
    Credit = models.IntegerField(default=0)
    
    USER   = 'user'
    VENDOR = 'vendor'
    ADMIN  = 'admin'
    ROLE_CHOICES = [(USER, 'کاربر'), (VENDOR, 'فروشنده'), (ADMIN, 'مدیر')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    