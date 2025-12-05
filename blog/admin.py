from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Post, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def post_count(self, obj):
        """Display count of posts in this category."""
        if obj and obj.pk:
            return obj.posts.count()
        return 0
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model."""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def post_count(self, obj):
        """Display count of posts with this tag."""
        if obj and obj.pk:
            return obj.posts.count()
        return 0
    post_count.short_description = 'Posts'


# CommentInline temporarily disabled to fix admin formset error
# Comments can be managed separately in the Comments admin section
# class CommentInline(admin.TabularInline):
#     """Inline comments for Post admin."""
#     model = Comment
#     extra = 0
#     readonly_fields = ['user', 'created_at']
#     fields = ['user', 'content', 'is_approved', 'created_at']
#     can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'published_at', 'comment_count', 'post_actions']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'author__username', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'published_at']
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']
    # Comment inline disabled temporarily to fix formset error
    # You can manage comments separately in the Comments admin section
    # inlines = [CommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author')
        }),
        ('Content', {
            'fields': ('content', 'image', 'category', 'tags')
        }),
        ('Status & Dates', {
            'fields': ('status', 'created_at', 'updated_at', 'published_at')
        }),
    )
    
    def comment_count(self, obj):
        """Display count of comments."""
        if obj and obj.pk:
            count = obj.comments.count()
            if count > 0:
                try:
                    url = reverse('admin:blog_comment_changelist') + f'?post__id__exact={obj.id}'
                    return format_html('<a href="{}">{}</a>', url, count)
                except:
                    return count
            return count
        return 0
    comment_count.short_description = 'Comments'
    
    def post_actions(self, obj):
        """Display action buttons."""
        if obj and obj.pk and obj.slug:
            try:
                view_url = reverse('blog:post_detail', kwargs={'slug': obj.slug})
                return format_html(
                    '<a href="{}" target="_blank" class="button">View</a>',
                    view_url
                )
            except:
                return '-'
        return '-'
    post_actions.short_description = 'Actions'
    
    def save_model(self, request, obj, form, change):
        """Set author to current user if creating new post."""
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        try:
            qs = super().get_queryset(request)
            return qs.select_related('author', 'category').prefetch_related('tags', 'comments')
        except:
            return super().get_queryset(request)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""
    list_display = ['content_preview', 'post_link', 'user', 'is_approved', 'created_at', 'comment_actions']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['content', 'user__username', 'post__title']
    readonly_fields = ['post', 'user', 'content', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_editable = ['is_approved']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'user', 'content', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def content_preview(self, obj):
        """Display truncated content."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def post_link(self, obj):
        """Link to post."""
        if obj and obj.post and obj.post.pk:
            try:
                url = reverse('admin:blog_post_change', args=[obj.post.pk])
                title = obj.post.title[:30] if obj.post.title else 'Post'
                return format_html('<a href="{}">{}</a>', url, title)
            except:
                return obj.post.title[:30] if obj.post.title else '-'
        return '-'
    post_link.short_description = 'Post'
    
    def comment_actions(self, obj):
        """Display action buttons."""
        if obj and obj.post and obj.post.slug and obj.pk:
            try:
                view_url = reverse('blog:post_detail', kwargs={'slug': obj.post.slug}) + f'#comment-{obj.id}'
                return format_html(
                    '<a href="{}" target="_blank" class="button">View Post</a>',
                    view_url
                )
            except:
                return '-'
        return '-'
    comment_actions.short_description = 'Actions'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        try:
            qs = super().get_queryset(request)
            return qs.select_related('post', 'user', 'post__author')
        except:
            return super().get_queryset(request)
