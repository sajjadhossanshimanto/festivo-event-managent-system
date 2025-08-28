from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
class CustomUser(AbstractUser):
    profile_image =  models.ImageField(
        upload_to='users/profile', blank=True, default="users/profile/default.png"
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'<CustomUser: {self.username}>'