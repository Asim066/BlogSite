"""
Permission utilities for role-based access control.
"""
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


def is_admin(user):
    """Check if user is in Admin group."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Admin').exists() or user.is_superuser


def is_author(user):
    """Check if user is in Author group."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Author').exists()


def is_reader(user):
    """Check if user is in Reader group."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Reader').exists()


def can_edit_post(user, post):
    """
    Check if user can edit a specific post.
    - Admin can edit any post
    - Author can only edit their own posts
    - Reader cannot edit posts
    """
    if not user.is_authenticated:
        return False
    
    if is_admin(user):
        return True
    
    if is_author(user) and post.author == user:
        return True
    
    return False


def can_delete_post(user, post):
    """
    Check if user can delete a specific post.
    - Admin can delete any post
    - Author can only delete their own posts
    - Reader cannot delete posts
    """
    if not user.is_authenticated:
        return False
    
    if is_admin(user):
        return True
    
    if is_author(user) and post.author == user:
        return True
    
    return False


def can_create_post(user):
    """
    Check if user can create posts.
    - Admin and Author can create posts
    - Reader cannot create posts
    """
    if not user.is_authenticated:
        return False
    
    return is_admin(user) or is_author(user)


def require_author_or_admin(user):
    """Raise PermissionDenied if user is not Author or Admin."""
    if not can_create_post(user):
        raise PermissionDenied("You don't have permission to perform this action.")


def require_post_owner_or_admin(user, post):
    """Raise PermissionDenied if user cannot edit the post."""
    if not can_edit_post(user, post):
        raise PermissionDenied("You don't have permission to edit this post.")

