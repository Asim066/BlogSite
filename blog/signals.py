"""
Signals for blog app.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Post


@receiver(pre_save, sender=Post)
def auto_generate_slug(sender, instance, **kwargs):
    """
    Auto-generate slug from title if not provided.
    This is a backup to the save() method in the model.
    """
    if not instance.slug:
        instance.slug = slugify(instance.title)
        # Ensure uniqueness
        original_slug = instance.slug
        counter = 1
        while Post.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1


@receiver(post_save, sender=Post)
def notify_admin_on_publish(sender, instance, created, **kwargs):
    """
    Notify admin when a post is published.
    This signal fires when a post status changes to published.
    """
    # Check if post was just published (status changed to published)
    if instance.status == Post.Status.PUBLISHED:
        # Get all admin users
        admin_users = User.objects.filter(
            is_superuser=True
        ) | User.objects.filter(
            groups__name='Admin'
        )
        
        # Send email notification to each admin (if email is configured)
        if admin_users.exists() and hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
            try:
                admin_emails = [admin.email for admin in admin_users if admin.email]
                if admin_emails:
                    subject = f'New Post Published: {instance.title}'
                    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
                    post_url = instance.get_absolute_url()
                    full_url = f"{site_url}{post_url}" if not post_url.startswith('http') else post_url
                    
                    message = f'''A new post has been published on the blog:

Title: {instance.title}
Author: {instance.author.get_full_name() or instance.author.username}
Category: {instance.category.name if instance.category else "None"}
Published: {instance.published_at or instance.created_at}

View the post: {full_url}
'''
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
                        admin_emails,
                        fail_silently=True,  # Don't raise errors if email fails
                    )
            except Exception as e:
                # Log error but don't break the save process
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error sending email notification: {e}')

