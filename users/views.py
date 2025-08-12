from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm
# from users.models import User
from users.forms import UserForm


# Participant:::
def participant_list(request):
    participants = User.objects.all()
    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_update(request, id):
    participant = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully!")
            return redirect('participant_list')
    else:
        form = UserForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form, 'participant': participant})

def participant_delete(request, id):
    participant = User.objects.get(id=id)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
        return redirect('participant_list')
    return render(request, 'events/participant_confirm_delete.html', {'participant': participant})


def signup_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

@login_required
def dashboard_view(request):
    # TODO:
    print(request.user.groups.name)
    if is_admin(request.user):
        return render(request, 'users/dashboard/admin.html')
    elif is_manager(request.user):
        return render(request, 'users/dashboard/manager.html')
    else:
        return render(request, 'users/dashboard/user.html')
