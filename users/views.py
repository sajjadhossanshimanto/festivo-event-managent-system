from django import forms
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from users.forms import LoginForm
from users.models import CustomUser
from users.forms import UserForm, UserEditForm


# permisiion functions
def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def no_permission(request):
    return render(request, 'users/unauthorized.html')

# participant-functions 
@login_required(login_url='login')
@permission_required('events.view_participant', login_url='no-permission')
def participant_list(request):
    participants = CustomUser.objects.all()
    return render(request, 'users/participant_list.html', {'participants': participants})

@login_required(login_url='login')
@permission_required('events.change_participant', login_url='no-permission')
def participant_update(request, id):
    participant = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=participant)

        if form.is_valid():
            # Check for username uniqueness only if changed
            username = form.cleaned_data.get('username')
            if CustomUser.objects.exclude(id=participant.id).filter(username=username).exists():
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

@login_required(login_url='login')
@permission_required('events.delete_participant', login_url='no-permission')
def participant_delete(request, id):
    participant = CustomUser.objects.get(id=id)
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "Activation email has been send")
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "Please activate your account first. Check your email for the activation link.")
                return render(request, 'users/login.html', {'form': form})
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def activate_user(request, user_id:int, token:str):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse("user does not exist")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account have been activated.")
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Invalid Id or token')
    
    return redirect("login")


# @login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def view_profile(request):
    return render(request, 'users/profile.html')