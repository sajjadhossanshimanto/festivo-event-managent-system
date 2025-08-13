from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
# from django.contrib.auth.forms import UserForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from users.forms import LoginForm
# from users.models import User
from users.forms import UserForm, UserEditForm


# permisiion functions
def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def no_permission(request):
    return render(request, 'users/unauthorized.html')

# participant-functions 
def participant_list(request):
    participants = User.objects.all()
    return render(request, 'users/participant_list.html', {'participants': participants})

def participant_update(request, id):
    participant = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=participant)

        if form.is_valid():
            # Check for username uniqueness only if changed
            username = form.cleaned_data.get('username')
            if User.objects.exclude(id=participant.id).filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
            else:
                user = form.save(commit=False)
                # Update role (group)
                role = form.cleaned_data.get('role')
                if role:
                    user.groups.clear()
                    user.groups.add(role)
                else:
                    user.groups.clear()
                user.save()
                messages.success(request, "Participant updated successfully!")
                return redirect('participant_list')
    else:
        form = UserEditForm(instance=participant)

        # Pre-select the user's current group
        user_groups = participant.groups.all()
        if user_groups.exists():
            form.fields['role'].initial = user_groups.first().id
    return render(request, 'users/participant_edit.html', {'form': form, 'participant': participant})

def participant_delete(request, id):
    participant = User.objects.get(id=id)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
        return redirect('participant_list')
    return render(request, 'users/participant_confirm_delete.html', {'participant': participant})


# login- logout
def signup_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# @login_required
def logout_view(request):
    logout(request)
    return redirect('login')

