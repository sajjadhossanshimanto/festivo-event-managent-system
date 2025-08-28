from django.contrib import admin
from events.models import Category, Event
from users.models import CustomUser


# Added this so that I can import data faster
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(CustomUser)