from django.shortcuts import render, redirect
from .models import Event, Category
from django.utils.timezone import now
from .forms import EventForm, CategoryForm
from django.contrib import messages
from django.db.models import Q

# List all events
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


    events = events.select_related('category').prefetch_related('participants').order_by('date', 'time')

    context = {
        'events': events,
        'categories': Category.objects.all(),
        'stats': {
            'total': Event.objects.count(),
            'past': Event.objects.filter(date__lt=today).count(),
            'upcoming': Event.objects.filter(date__gt=today).count(),
            'today': Event.objects.filter(date=today).count(),
            'total_participants': Participant.objects.count(),
        }
    }
    return render(request, 'events/event_list.html', context)


# Event detail view
def event_detail(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/event_detail.html', {'event': event})

# Create new event
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

# Update an event
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

# Delete an event
def event_delete(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# Participant:::
# List all participants
def participant_list(request):
    participants = Participant.objects.all().order_by('name')
    return render(request, 'events/participant_list.html', {'participants': participants})

# Create a new participant
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant added successfully!")
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form})

# Update participant
def participant_update(request, id):
    participant = Participant.objects.get(id=id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully!")
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form, 'participant': participant})

# Delete participant
def participant_delete(request, id):
    participant = Participant.objects.get(id=id)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
        return redirect('participant_list')
    return render(request, 'events/participant_confirm_delete.html', {'participant': participant})


# Category:::
# List Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

# Create Category
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

# Update Category
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

# Delete Category
def category_delete(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})


