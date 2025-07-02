from django.contrib import admin
from .models import Category, Event, Participant

# Added this so that I can import data faster
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Participant)
