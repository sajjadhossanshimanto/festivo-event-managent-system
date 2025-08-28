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
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from users.models import CustomUser
from users.forms import UserForm, UserEditForm, ChangePasswordForm, CustomSetPassword


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

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = CustomUser.objects.filter(email=email)
            if users.exists():
                user = users.first()
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(f"/reset/{uid}/{token}/")
                subject = "Festivo Password Reset"
                message = render_to_string("users/password_reset_email.txt", {"reset_url": reset_url, "user": user})
                send_mail(subject, message, None, [email])
                messages.success(request, "Password reset link sent to your email.")
                return redirect("login")
            else:
                form.add_error("email", "No user found with this email.")
    else:
        form = PasswordResetForm()
    return render(request, "users/password_reset.html", {"form": form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPassword(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been reset. You can now log in.")
                return redirect("login")
        else:
            form = CustomSetPassword(user)
        return render(request, "users/password_reset_confirm.html", {"form": form})
    else:
        return HttpResponse("Invalid password reset link.")

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
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            logout(request)
            return redirect('login')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required(login_url='login')
def view_profile(request):
    return render(request, 'users/profile.html')