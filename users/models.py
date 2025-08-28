from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
class CustomUser(AbstractUser):
    profile_image =  models.ImageField(
        upload_to='users/profile', blank=True, default="users/profile/default.png"
    )
    bio = models.TextField(blank=True)
    last_update = models.DateTimeField(auto_now=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        help_text="Enter a valid phone number (e.g. +8801234567890)",
        verbose_name="Phone Number",
    )

    def clean(self):
        super().clean()
        import re
        if self.phone_number:
            pattern = r"^\+?\d{10,15}$"
            if not re.match(pattern, self.phone_number):
                from django.core.exceptions import ValidationError
                raise ValidationError({
                    'phone_number': "Enter a valid phone number (10-15 digits, optional '+')."
                })

    def __str__(self):
        return f'<CustomUser: {self.username}>'