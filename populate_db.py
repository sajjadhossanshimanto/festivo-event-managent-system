import os
import random

import django
from django.contrib.auth.models import Group
from faker import Faker

from events.models import Category, Event
from users.models import CustomUser

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()



def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Projects
    categories = [Category.objects.create(
        name=fake.bs().capitalize(),
        description=fake.paragraph(),
    ) for _ in range(5)]
    print(f"Created {len(categories)} projects.")

    # Create Employees
    persons = []
    for _ in range(20):
        person = CustomUser.objects.create(
            username = fake.name(),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email = fake.email()
        )
        person.is_active = True
        persons.append(person)
    print(f'created {len(persons)} persons`')
    
    for _ in range(10):
        u = Event.objects.create(
            name = fake.sentence(),
            description = fake.paragraph(),
            date = fake.date(),
            time = fake.time(),
            location = " ".join(fake.location_on_land()[2:]),
            category = random.choice(categories)
        )
        u.rsvp.set(random.sample(persons, random.randint(1, 3)))

    
    print(f"Created 20 tasks.")
