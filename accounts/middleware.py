"""
Middleware for user activity tracking and default role assignment.
"""
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in


class AssignDefaultRoleMiddleware:
    """
    Middleware to assign default Reader role to new users.
    This runs after user registration/login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Assign default Reader role if user has no groups (fallback only)
        # Note: Role should be assigned during registration, this is just a safety net
        if request.user.is_authenticated and not request.user.is_superuser:
            if not request.user.groups.exists():
                try:
                    reader_group = Group.objects.get(name='Reader')
                    request.user.groups.add(reader_group)
                except Group.DoesNotExist:
                    # Groups not created yet, skip silently
                    pass

        response = self.get_response(request)
        return response


class UserActivityMiddleware:
    """
    Middleware to track user activity (last_seen timestamp).
    Requires a UserProfile model with last_seen field, or can be added later.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last_seen timestamp
            # Note: This requires a UserProfile model or extending User model
            # For now, we'll just track in session
            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response

