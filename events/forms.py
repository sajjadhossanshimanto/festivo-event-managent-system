from django import forms
from .models import Event, Category

DEFAULT_CLASSES = (
    "block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-700 " 
    "placeholder-gray-400 focus:border-blue-500 focus:ring focus:ring-blue-300 focus:ring-opacity-50"
)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image_link', 'name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'image_link': forms.URLInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter image URL',
            }),
            'name': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter event name',
                'maxlength': '200',
            }),
            'description': forms.Textarea(attrs={
                'class': DEFAULT_CLASSES + " resize-none",
                'placeholder': 'Enter event description',
                'rows': 3,
            }),
            'date': forms.DateInput(attrs={
                'class': DEFAULT_CLASSES,
                'type': 'date',
            }),
            'time': forms.TimeInput(attrs={
                'class': DEFAULT_CLASSES,
                'type': 'time',
            }),
            'location': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter event location',
            }),
            'category': forms.Select(attrs={
                'class': DEFAULT_CLASSES,
            }),
        }
        labels = {
            'image_link': 'Image URL',
            'name': 'Event Name',
            'description': 'Description',
            'date': 'Date',
            'time': 'Time',
            'location': 'Location',
            'category': 'Category',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter category name',
            }),
            'description': forms.Textarea(attrs={
                'class': DEFAULT_CLASSES + " resize-none",
                'rows': 3,
            }),
        }

