from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib import messages
from django.shortcuts import redirect


# Unregister default Group admin and register custom one to fix Python 3.14.1 compatibility issue
try:
    admin.site.unregister(Group)
except:
    pass  # Group might not be registered yet


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    """Custom Group admin to work around Python 3.14.1 + Django 4.2.27 compatibility issue."""
    
    def add_view(self, request, form_url='', extra_context=None):
        """Redirect to a helpful message instead of showing the broken form."""
        try:
            messages.warning(request, 
                '⚠️ Due to a compatibility issue between Python 3.14.1 and Django 4.2.27, '
                'groups cannot be added through the admin panel.\n\n'
                '✅ SOLUTION: Use the management command instead:\n'
                '   python manage.py setup_groups\n\n'
                'Or use Django shell to create groups manually.')
            return redirect('admin:auth_group_changelist')
        except:
            # Fallback if redirect fails
            from django.http import HttpResponse
            return HttpResponse(
                'Groups cannot be added via admin. Use: python manage.py setup_groups',
                status=200
            )
    
    def has_add_permission(self, request):
        """Disable add permission to prevent the error."""
        return False
