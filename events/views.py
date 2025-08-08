from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from events.models import Event, Category
from events.forms import EventForm, CategoryForm
from users.views import *


def event_list(request):
    today = now().date()
    type = request.GET.get('type', 'today')
    # type = type if type in ['past', 'upcoming', 'all'] else 'today'
    category_filter = request.GET.get('category')

    events = Event.objects.all()

    # Category-based 
    if category_filter:
        type = 'all'  
        events = events.filter(category__id=category_filter)

    # Date-based 
    if type == 'past':
        events = events.filter(date__lt=today)
    elif type == 'upcoming':
        events = events.filter(date__gt=today)
    elif type == 'today':
        events = events.filter(date=today)


    search_query = request.GET.get('q')

    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )


    events = events.select_related('category').prefetch_related('rsvp').order_by('date', 'time')

    context = {
        'events': events,
        'categories': Category.objects.all(),
        'stats': {
            'total': Event.objects.count(),
            'past': Event.objects.filter(date__lt=today).count(),
            'upcoming': Event.objects.filter(date__gt=today).count(),
            'today': Event.objects.filter(date=today).count(),
            'total_participants': User.objects.count(),
        }
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/event_detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

def event_update(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'event': event})

def event_delete(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# Category:::
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})

def category_update(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form, 'category': category})

def category_delete(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})


