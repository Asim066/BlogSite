from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class UserRegistrationForm(UserCreationForm):
    """Custom registration form with email field and role selection."""
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    
    ROLE_CHOICES = [
        ('reader', 'User/Reader - View posts and comment'),
        ('author', 'Author - Create, edit, and manage your own posts'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        help_text='Select your role. You can view and comment on posts as a User, or create and manage posts as an Author.',
        initial='reader'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name != 'role':  # Role uses RadioSelect, not form-control
                field.widget.attrs['class'] = 'form-control'
            if field.required and field_name != 'role':
                field.widget.attrs['required'] = 'required'

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        """Save user, set email, and assign role."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        role = self.cleaned_data.get('role', 'reader')
        
        if commit:
            user.save()
            # Assign the selected role
            try:
                if role == 'author':
                    author_group = Group.objects.get(name='Author')
                    user.groups.add(author_group)
                else:  # reader
                    reader_group = Group.objects.get(name='Reader')
                    user.groups.add(reader_group)
            except Group.DoesNotExist:
                # Groups not created yet, will be assigned by middleware
                pass
        
        return user

