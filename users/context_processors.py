from users.models import Friendship


def pending_requests(request):
    """Makes pending_requests count available in every template automatically."""
    if request.user.is_authenticated:
        count = Friendship.objects.filter(
            to_user=request.user,
            status='pending'
        ).count()
        return {'pending_requests': count}
    return {'pending_requests': 0}