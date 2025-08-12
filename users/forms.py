from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


DEFAULT_CLASSES = (
    "block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-700 " 
    "placeholder-gray-400 focus:border-blue-500 focus:ring focus:ring-blue-300 focus:ring-opacity-50"
)

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-1 border rounded-lg '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': field.label
            })

            if field.help_text:
                field.help_text = f'<span class="block mt-1 text-sm text-gray-500">{field.help_text}</span>'

class LoginForm(AuthenticationForm):
    pass