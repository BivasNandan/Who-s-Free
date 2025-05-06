from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, ChatMessage
from users.models import CustomUser, Friendship
from django.db.models import Q

@login_required
def chat_room(request, user_id):
    """
    View to handle one-on-one chat between two users.
    Only friends can chat.
    """
    other_user = get_object_or_404(CustomUser, id=user_id)

    # Check if the other user is a friend
    is_friend = Friendship.objects.filter(
        (Q(from_user=request.user, to_user=other_user) | Q(from_user=other_user, to_user=request.user)),
        status='accepted'
    ).exists()

    if not is_friend:
        messages.error(request, "You can only chat with your friends.")
        return redirect('friend_list')  # Redirect to the friend list page

    # Check if a chat room already exists between the two users
    chat_room = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat_room:
        chat_room = ChatRoom.objects.create()
        chat_room.participants.add(request.user, other_user)

    # Retrieve chat messages for this room
    messages_history = ChatMessage.objects.filter(room=chat_room).order_by('timestamp')

    return render(request, 'chat/chat_room.html', {
        'room_name': chat_room.id,  # Use the chat room ID as the room name
        'username': request.user.username,
        'other_user': other_user,
        'messages_history': messages_history,
    })