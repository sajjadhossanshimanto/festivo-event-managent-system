from django.urls import path
from users.views import participant_list, participant_create, participant_update, participant_delete


urlpatterns = [
    path('participants/', participant_list, name='participant_list'),
    path('participants/create/', participant_create, name='participant_create'),
    path('participants/<int:id>/edit/', participant_update, name='participant_update'),
    path('participants/<int:id>/delete/', participant_delete, name='participant_delete'),
]