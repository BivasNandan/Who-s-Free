from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm

@login_required
def create_event(request):
    if request.method == 'POST':  # Fixed request method check
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'The Event was created successfully!')  # Fixed messages.success
            return redirect('events_list')  # Fixed redirect
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def update_event(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)  # Ensure only the creator can update
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES, instance=event)  # Fixed instance binding
        if form.is_valid():
            form.save()
            messages.success(request, 'The event has been updated successfully!')  # Fixed messages.success
            return redirect('events_list')  # Fixed redirect
    else:
        form = EventForm(instance=event)  # Fixed instance binding
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)  # Ensure only the creator can delete
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'The event has been deleted successfully!')
        return redirect('events_list')
    return render(request, 'events/delete_event.html', {'event': event})

@login_required
def events_list(request):
    events = Event.objects.all()
    return render(request, 'events/events_list.html', {'events': events, 'user': request.user})

@login_required
def mark_interested(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != request.user:  # Prevent marking your own event as interested
        event.interested_users.add(request.user)
        messages.success(request, 'You are now interested in this event!')
        return redirect('my_interested_event')
    else:
        messages.error(request, 'You cannot mark your own event as interested.')
    return redirect('events_list')

@login_required
def my_created_events(request):
    events = Event.objects.filter(user=request.user)  # Filter events created by the logged-in user
    return render(request, 'events/my_created_events.html', {'events': events})

@login_required
def my_interested_event(request):
    events = Event.objects.filter(interested_users=request.user)
    return render(request, 'events/my_interested_event.html', {'events': events})

@login_required
def interested_users(request, id):
    event = get_object_or_404(Event, id = id, user = request.user)
    interested_users = event.interested_users.all()
    return render(request, 'events/interested_users.html', {'event': event, 'interested_users': interested_users})
