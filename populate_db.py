import os
import django
from faker import Faker
import random
from events.models import Category, Event, Participant
from django.contrib.auth.models import Group

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
    events = []
    for _ in range(10):
        u = Event.objects.create(
            name = fake.sentence(),
            description = fake.paragraph(),
            date = fake.date(),
            time = fake.time(),
            location = " ".join(fake.location_on_land()[2:]),
            category = random.choice(categories)
        )
        events.append(u)
    print(f"Created {len(events)} employees.")

    # Create Tasks
    for _ in range(20):
        person = Participant.objects.create(
            name = fake.name(),
            email = fake.email()
        )
        person.events.set(random.sample(events, random.randint(1, 3)))

    print(f"Created 20 tasks.")
