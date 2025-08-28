from django.urls import path
from users.views import participant_list, participant_update, participant_delete, no_permission, view_profile, password_reset_request, password_reset_confirm
from users import views


urlpatterns = [
    path('participants/', participant_list, name='participant_list'),
    path('participants/<int:id>/edit/', participant_update, name='participant_update'),
    path('participants/<int:id>/delete/', participant_delete, name='participant_delete'),
    
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<int:user_id>/<str:token>/', views.activate_user),

    path('profile', view_profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),

    path("unauthurized/", no_permission, name='no-permission'),

    # Password reset
    path('password-reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]