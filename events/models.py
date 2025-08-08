from django.db import models
from django.contrib.auth.models import User


def file_location(instance, filename):
    return f'events/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    image = models.ImageField(upload_to=file_location, null=True, blank=True, default=file_location('', 'default.png'))
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    rsvp = models.ManyToManyField(User, related_name='rsvp')

    def __str__(self):
        return self.name

