from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django import forms
from django.contrib.auth.hashers import check_password
from users.models import CustomUser



class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_image', 'username', 'first_name', 'last_name',
            'email', 'phone_number', 'password1', 'password2', 'bio'
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
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone_number'
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

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-1 border rounded-lg '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': field.label
            })

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Incorrect current password.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "New passwords do not match.")
        return cleaned_data

class CustomSetPassword(SetPasswordForm):
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
