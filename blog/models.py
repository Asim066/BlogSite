from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Category model for organizing posts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL for category posts."""
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Tag model for post tagging."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL for tag posts."""
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class PublishedManager(models.Manager):
    """Custom manager for published posts."""
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Post model for blog entries."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Managers
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager for published posts

    class Meta:
        ordering = ['-created_at']
        default_permissions = ('add', 'change', 'delete', 'view')
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Set published_at when status changes to published
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        elif self.status == self.Status.DRAFT:
            self.published_at = None
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL for post detail."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        """Check if post is published."""
        return self.status == self.Status.PUBLISHED


class Comment(models.Model):
    """Comment model for post comments."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        default_permissions = ('add', 'change', 'delete', 'view')
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

    def get_absolute_url(self):
        """Return URL to post with comment anchor."""
        return f"{self.post.get_absolute_url()}#comment-{self.id}"
