from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q

from events.models import Event, Category
from events.forms import EventForm, CategoryForm
from users.views import is_admin, is_manager


# :: events related functions ::

@login_required(login_url='login')
@permission_required('events.view_event', login_url='no-permission')
def event_list(request):
    user = request.user
    today = now().date()
    type_ = request.GET.get('type', 'all')
    # type = type if type in ['past', 'upcoming', 'all'] else 'today'
    category_filter = request.GET.get('category')

    events = Event.objects.all()

    # Category-based 
    if category_filter:
        type_ = 'all'
        events = events.filter(category__id=category_filter)


    if type_ == 'past':
        events = events.filter(date__lt=today)
    elif type_ == 'upcoming':
        events = events.filter(date__gt=today)
    elif type_ == 'today':
        events = events.filter(date=today)
    elif type_ == 'rsvp':
        events = user.rsvp.all()

    search_query = request.GET.get('q')

    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query) 
        )


    events = events.select_related('category').prefetch_related('rsvp').order_by('date', 'time')
    rsvp_items = user.rsvp.values_list('id', flat=True)
    # print(rsvp_items)

    context = {
        'events': events,
        'categories': Category.objects.all(),
        'stats': {
            'total': Event.objects.count(),
            'total_rspv': len(rsvp_items),
            'past': Event.objects.filter(date__lt=today).count(),
            'upcoming': Event.objects.filter(date__gt=today).count(),
            'today': Event.objects.filter(date=today).count(),
        },
        'rsvp_items': rsvp_items,
    }
    return render(request, 'events/event_list.html', context)

@login_required(login_url='login')
@permission_required('events.view_event', login_url='no-permission')
def event_detail(request, id):
    event = Event.objects.get(id=id)
    edit_right = is_admin(request.user) or is_manager(request.user)
    return render(request, 'events/event_detail.html', {'event': event, 'edit_right': edit_right})

@login_required(login_url='login')
@permission_required('events.add_event', login_url='no-permission')
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

@login_required(login_url='login')
@permission_required('events.change_event', login_url='no-permission')
def event_update(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'event': event})

@login_required(login_url='login')
@permission_required('events.delete_event', login_url='no-permission')
def event_delete(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required(login_url='login')
def rsvp_event(request, user_id, event_id):
    # print(user_id, event_id)
    Event.objects.get(id=event_id).rsvp.add(User.objects.get(id=user_id))
    messages.success(request, "Rsvp was sucessfull")
    return redirect('event_list')

# :: Category ::
@login_required(login_url='login')
@permission_required('events.view_category', login_url='no-permission')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

@login_required(login_url='login')
@permission_required('events.add_category', login_url='no-permission')
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

@login_required(login_url='login')
@permission_required('events.change_category', login_url='no-permission')
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

@login_required(login_url='login')
@permission_required('events.delete_category', login_url='no-permission')
def category_delete(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})


# :: Uncatagory ::

def dashboard(request):
    return render(request, 'events/intro.html')
