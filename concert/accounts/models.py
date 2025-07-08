from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    ProfileImage = models.ImageField(upload_to="profileImages/")

    Man = 1
    Woman = 2
    status_choices = ((Man,"مرد"),(Woman,"زن"))
    Gender = models.IntegerField(choices=status_choices)
    
    Credit = models.IntegerField(default=0)
    