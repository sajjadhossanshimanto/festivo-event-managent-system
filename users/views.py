from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



# Participant:::
def participant_list(request):
    participants = User.objects.all()
    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant added successfully!")
            return redirect('participant_list')
    else:
        form = UserCreationForm()
    return render(request, 'events/participant_form.html', {'form': form})

def participant_update(request, id):
    participant = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully!")
            return redirect('participant_list')
    else:
        form = UserCreationForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form, 'participant': participant})

def participant_delete(request, id):
    participant = User.objects.get(id=id)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
        return redirect('participant_list')
    return render(request, 'events/participant_confirm_delete.html', {'participant': participant})
