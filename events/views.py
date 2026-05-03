from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'The Event was created successfully!')
            return redirect('events_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def update_event(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'The event has been updated successfully!')
            return redirect('events_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'The event has been deleted successfully!')
        return redirect('events_list')
    return render(request, 'events/delete_event.html', {'event': event})


@login_required
def events_list(request):
    events = Event.objects.all().order_by('-start_time')
    return render(request, 'events/events_list.html', {'events': events, 'user': request.user})


@login_required
def mark_interested(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != request.user:
        if request.user in event.interested_users.all():
            event.interested_users.remove(request.user)
            messages.success(request, 'Removed from your interested events.')
        else:
            event.interested_users.add(request.user)
            messages.success(request, 'You are now interested in this event!')
        return redirect('events_list')
    else:
        messages.error(request, 'You cannot mark your own event as interested.')
    return redirect('events_list')


@login_required
def my_created_events(request):
    events = Event.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'events/my_created_events.html', {'events': events})


@login_required
def my_interested_event(request):
    events = Event.objects.filter(interested_users=request.user).order_by('-start_time')
    return render(request, 'events/my_interested_event.html', {'events': events})


@login_required
def interested_users(request, id):
    # ── FIX: removed user=request.user so ANY logged-in user can see who's going ──
    event = get_object_or_404(Event, id=id)
    interested = event.interested_users.all()
    return render(request, 'events/interested_users.html', {
        'event': event,
        'interested_users': interested,
    })