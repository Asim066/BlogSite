from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm


class RegisterView(CreateView):
    """User registration view."""
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        """Process valid form, assign role, and log user in."""
        # Save the user (this also assigns the role via form.save())
        user = form.save()
        
        # Ensure role is assigned (in case groups don't exist yet)
        role = form.cleaned_data.get('role', 'reader')
        try:
            if role == 'author':
                author_group = Group.objects.get(name='Author')
                user.groups.add(author_group)
                messages.success(self.request, f'Welcome, {user.username}! Your Author account has been created. You can now create and manage posts.')
            else:
                reader_group = Group.objects.get(name='Reader')
                user.groups.add(reader_group)
                messages.success(self.request, f'Welcome, {user.username}! Your account has been created. You can view posts and comment.')
        except Group.DoesNotExist:
            messages.warning(self.request, 'Account created, but role assignment failed. Please contact an administrator.')
        
        # Log the user in
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        
        return redirect(self.success_url)

    def form_invalid(self, form):
        """Handle invalid form."""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@login_required
def profile_view(request):
    """User profile view."""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
