from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q

from events.models import Event, Category
from events.forms import EventForm, CategoryForm
from users.views import is_admin, is_manager


# :: events related functions ::


class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    permission_required = 'events.view_event'
    login_url = 'login'
    raise_exception = False
    redirect_field_name = None
    def get_queryset(self):
        user = self.request.user
        today = now().date()
        type_ = self.request.GET.get('type', 'all')
        category_filter = self.request.GET.get('category')
        events = Event.objects.all()
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
        search_query = self.request.GET.get('q')
        if search_query:
            events = events.filter(
                Q(name__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return events.select_related('category').prefetch_related('rsvp').order_by('date', 'time')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = now().date()
        rsvp_items = user.rsvp.values_list('id', flat=True)
        context['categories'] = Category.objects.all()
        context['stats'] = {
            'total': Event.objects.count(),
            'total_rspv': len(rsvp_items),
            'past': Event.objects.filter(date__lt=today).count(),
            'upcoming': Event.objects.filter(date__gt=today).count(),
            'today': Event.objects.filter(date=today).count(),
        }
        context['rsvp_items'] = rsvp_items
        return context


class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    permission_required = 'events.view_event'
    login_url = 'login'
    pk_url_kwarg = 'id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_right'] = is_admin(self.request.user) or is_manager(self.request.user)
        return context


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    permission_required = 'events.add_event'
    login_url = 'login'
    success_url = reverse_lazy('event_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Event created successfully!')
        return response

class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    permission_required = 'events.change_event'
    login_url = 'login'
    pk_url_kwarg = 'id'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Event updated successfully!')
        return response
    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'id': self.object.id})

class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    permission_required = 'events.delete_event'
    login_url = 'login'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('event_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)

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
