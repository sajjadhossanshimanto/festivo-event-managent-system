from django.urls import path
from users.views import participant_list, participant_update, participant_delete
from users import views


urlpatterns = [
    path('participants/', participant_list, name='participant_list'),
    path('participants/<int:id>/edit/', participant_update, name='participant_update'),
    path('participants/<int:id>/delete/', participant_delete, name='participant_delete'),
    
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]