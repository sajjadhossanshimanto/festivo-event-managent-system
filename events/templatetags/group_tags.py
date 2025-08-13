from django import template
from django.contrib.auth.models import Group

from users.views import is_admin, is_manager


register = template.Library()

user_features = (
    ('View All Events', 'event_list'),
    ('Logout', 'logout'),
)
manager_features = (
    ('Create Event', 'event_create'),
    ('Categories', 'category_list'),
) + user_features
admin_features = (
    ('Manage Accounts', 'participant_list'),
) + manager_features


@register.simple_tag(takes_context=True)
def group_features(context):
    user = context['user']
    if not user.is_authenticated:
        return [('Login', 'login')]
    elif is_admin(user):
        return admin_features
    elif is_manager(user):
        return manager_features
    else:
        return user_features