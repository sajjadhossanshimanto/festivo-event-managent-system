from django.urls import path
from events.views import event_list, event_detail, event_create, event_update, event_delete, category_list, category_create, category_update, category_delete

urlpatterns = [
    path('', event_list, name='event_list'),
    path('events/', event_list, name='event_list'),
    path('events/<int:id>/', event_detail, name='event_detail'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:id>/edit/', event_update, name='event_update'),
    path('events/<int:id>/delete/', event_delete, name='event_delete'),
    path('categories/', category_list, name='category_list'),
    path('categories/add/', category_create, name='category_create'),
    path('categories/<int:id>/edit/', category_update, name='category_update'),
    path('categories/<int:id>/delete/', category_delete, name='category_delete'),
]
