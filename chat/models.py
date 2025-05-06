from django.db import models
from users.models import CustomUser

class ChatRoom(models.Model):
    """
    Represents a one-on-one chat room between two individual users.
    """
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')  # Two users in the chat room
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id'],  # Ensure unique chat rooms for each pair of users
                name='unique_chat_room'
            )
        ]

    def __str__(self):
        return f"ChatRoom between {', '.join([user.username for user in self.participants.all()])}"

class ChatMessage(models.Model):
    """
    Represents individual messages sent in a chat room.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')  # Chat room the message belongs to
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')  # User who sent the message
    content = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)  # When the message was sent

    def __str__(self):
        return f"Message from {self.sender.username} in {self.room}"


class TypingIndicator(models.Model):
    """
    Tracks when a user is typing in a chat room.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='typing_indicators')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='typing_status')
    is_typing = models.BooleanField(default=False)  # True if the user is typing

    def __str__(self):
        return f"{self.user.username} is typing in {self.room}" if self.is_typing else f"{self.user.username} stopped typing"


class MessageAttachment(models.Model):
    """
    Handles file attachments in messages.
    """
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='chat_attachments/')  # Path to store uploaded files
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.message}"