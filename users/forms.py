from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms



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

# Form for editing users (no password fields)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'] = forms.ModelChoiceField(
            queryset=Group.objects.all(),
            required=False,
            label='Role',
            widget=forms.Select(attrs={
                'class': 'w-full px-4 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            })
        )
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-1 border rounded-lg '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': field.label
            })

class LoginForm(AuthenticationForm):
    pass