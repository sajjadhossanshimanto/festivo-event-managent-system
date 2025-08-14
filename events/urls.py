from django.urls import path
from events.views import (
    dashboard,
    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView,
    rsvp_event,
    category_list, category_create, category_update, category_delete
)

urlpatterns = [
    path('', dashboard, name='home'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event_detail'),
    path('events/create/', EventCreateView.as_view(), name='event_create'),
    path('events/<int:id>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('events/<int:id>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('events/rsvp/<int:user_id>/<int:event_id>/', rsvp_event, name='rsvp_event'),
    
    path('categories/', category_list, name='category_list'),
    path('categories/add/', category_create, name='category_create'),
    path('categories/<int:id>/edit/', category_update, name='category_update'),
    path('categories/<int:id>/delete/', category_delete, name='category_delete'),
]
