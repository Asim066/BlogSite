"""
Management command to create default user groups.
Run: python manage.py setup_groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post, Comment


class Command(BaseCommand):
    help = 'Creates default user groups (Admin, Author, Reader) with appropriate permissions'

    def handle(self, *args, **options):
        # Get content types
        post_content_type = ContentType.objects.get_for_model(Post)
        comment_content_type = ContentType.objects.get_for_model(Comment)

        # Get all permissions
        post_permissions = Permission.objects.filter(content_type=post_content_type)
        comment_permissions = Permission.objects.filter(content_type=comment_content_type)

        # Create Admin group (all permissions)
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            admin_group.permissions.set(Permission.objects.all())
            self.stdout.write(self.style.SUCCESS('✓ Created Admin group with all permissions'))
        else:
            self.stdout.write(self.style.WARNING('Admin group already exists'))

        # Create Author group (can create/edit/delete own posts, can moderate comments)
        author_group, created = Group.objects.get_or_create(name='Author')
        if created:
            # Post permissions: add, change, delete (for own posts - enforced in views)
            author_group.permissions.add(*post_permissions)
            # Comment permissions: add, change, delete (for moderation)
            author_group.permissions.add(*comment_permissions)
            self.stdout.write(self.style.SUCCESS('✓ Created Author group with post and comment permissions'))
        else:
            self.stdout.write(self.style.WARNING('Author group already exists'))

        # Create Reader group (can view and comment)
        reader_group, created = Group.objects.get_or_create(name='Reader')
        if created:
            # Post permissions: view only
            try:
                view_post = Permission.objects.get(codename='view_post', content_type=post_content_type)
                reader_group.permissions.add(view_post)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING('view_post permission not found - run migrations first'))
            
            # Comment permissions: add (to comment)
            try:
                add_comment = Permission.objects.get(codename='add_comment', content_type=comment_content_type)
                reader_group.permissions.add(add_comment)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING('add_comment permission not found - run migrations first'))
            
            self.stdout.write(self.style.SUCCESS('✓ Created Reader group with view and comment permissions'))
        else:
            self.stdout.write(self.style.WARNING('Reader group already exists'))

        self.stdout.write(self.style.SUCCESS('\n✓ All groups created successfully!'))

