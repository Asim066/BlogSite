from django import forms
from .models import Post, Category, Tag, Comment


class PostForm(forms.ModelForm):
    """Form for creating and updating posts."""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 20
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '5'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category optional
        self.fields['category'].required = False
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        # Make tags optional
        self.fields['tags'].required = False
        self.fields['tags'].queryset = Tag.objects.all().order_by('name')
        # Make image optional
        self.fields['image'].required = False


class CommentForm(forms.ModelForm):
    """Form for adding comments."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''

