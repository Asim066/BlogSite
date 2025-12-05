from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm
from accounts.permissions import (
    can_create_post, can_edit_post, can_delete_post,
    require_author_or_admin, require_post_owner_or_admin
)


class PostListView(ListView):
    """Display paginated list of published posts."""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        """Return only published posts, ordered by newest first."""
        queryset = Post.published.all()
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        context['tags'] = Tag.objects.all().order_by('name')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    """Display a single post with comments."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Allow viewing published posts or own drafts."""
        user = self.request.user
        if user.is_authenticated:
            # Show published posts or user's own drafts
            return Post.objects.filter(
                Q(status=Post.Status.PUBLISHED) |
                Q(author=user, status=Post.Status.DRAFT)
            )
        # Anonymous users only see published posts
        return Post.published.all()

    def get_context_data(self, **kwargs):
        """Add comments and related posts."""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user
        
        # Get approved comments for public, or all comments for post author/admin
        if user.is_authenticated and (user.is_superuser or 
                                      user.groups.filter(name='Admin').exists() or 
                                      post.author == user):
            # Show all comments (approved and pending) to post author/admin
            context['comments'] = post.comments.all()
        else:
            # Show only approved comments to public
            context['comments'] = post.comments.filter(is_approved=True)
        
        context['comment_count'] = post.comments.filter(is_approved=True).count()
        context['comment_form'] = CommentForm()
        
        # Get related posts (same category, excluding current post)
        if post.category:
            context['related_posts'] = Post.published.filter(
                category=post.category
            ).exclude(pk=post.pk)[:3]
        else:
            context['related_posts'] = Post.published.exclude(pk=post.pk)[:3]
        
        return context


class CategoryPostListView(ListView):
    """Display posts filtered by category."""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        """Filter posts by category slug."""
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.published.filter(category=category)

    def get_context_data(self, **kwargs):
        """Add category to context."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context


class TagPostListView(ListView):
    """Display posts filtered by tag."""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        """Filter posts by tag slug."""
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.published.filter(tags=tag)

    def get_context_data(self, **kwargs):
        """Add tag to context."""
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return context


class AuthorDashboardView(ListView):
    """Dashboard for authors to manage their posts."""
    model = Post
    template_name = 'blog/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        """Check if user can create posts."""
        require_author_or_admin(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return user's posts, or all posts if admin."""
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Admin').exists():
            return Post.objects.all().order_by('-created_at')
        # Authors see only their own posts
        return Post.objects.filter(author=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Add statistics."""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_posts'] = queryset.count()
        context['published_posts'] = queryset.filter(status=Post.Status.PUBLISHED).count()
        context['draft_posts'] = queryset.filter(status=Post.Status.DRAFT).count()
        return context


class CreatePostView(CreateView):
    """Create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Check if user can create posts."""
        require_author_or_admin(request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set author to current user."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to dashboard after creation."""
        return reverse_lazy('blog:dashboard')


class UpdatePostView(UpdateView):
    """Update an existing post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        """Check if user can edit this post."""
        post = self.get_object()
        require_post_owner_or_admin(request.user, post)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Show success message."""
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to post detail or dashboard."""
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})


class DeletePostView(DeleteView):
    """Delete a post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        """Check if user can delete this post."""
        post = self.get_object()
        require_post_owner_or_admin(request.user, post)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Show success message and delete."""
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """Redirect to dashboard after deletion."""
        return reverse_lazy('blog:dashboard')


@login_required
def add_comment(request, slug):
    """Add a comment to a post with spam prevention."""
    post = get_object_or_404(Post, slug=slug)
    
    # Spam prevention: Check if user commented recently (within last 30 seconds)
    session_key = f'last_comment_time_{post.id}'
    last_comment_time = request.session.get(session_key)
    
    if last_comment_time:
        last_time = datetime.fromisoformat(last_comment_time)
        if datetime.now() - last_time < timedelta(seconds=30):
            messages.error(request, 'Please wait a moment before posting another comment.')
            return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            
            # Auto-approve comments from admins/authors, others need moderation
            if request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Author']).exists():
                comment.is_approved = True
            else:
                comment.is_approved = True  # Auto-approve by default (can be changed)
                # Uncomment below to require moderation for non-admin/author users:
                # comment.is_approved = False
            
            comment.save()
            
            # Update session with comment time
            request.session[session_key] = datetime.now().isoformat()
            
            messages.success(request, 'Your comment has been posted!')
            return redirect('blog:post_detail', slug=slug)
    else:
        form = CommentForm()
    
    return redirect('blog:post_detail', slug=slug)


@login_required
def approve_comment(request, comment_id):
    """Approve a comment (admin/author only)."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Check permissions: Admin or post author can moderate
    if not (request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists() or
            (request.user.groups.filter(name='Author').exists() and post.author == request.user)):
        messages.error(request, 'You do not have permission to moderate comments.')
        return redirect('blog:post_detail', slug=post.slug)
    
    comment.is_approved = True
    comment.save()
    messages.success(request, 'Comment approved successfully!')
    return redirect('blog:post_detail', slug=post.slug)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment (admin/author/comment owner)."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Check permissions: Admin, post author, or comment owner can delete
    if not (request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists() or
            (request.user.groups.filter(name='Author').exists() and post.author == request.user) or
            comment.user == request.user):
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('blog:post_detail', slug=post.slug)
    
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', slug=post.slug)


@login_required
def comment_moderation(request):
    """View all comments for moderation (admin/author)."""
    # Check if user can moderate
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Admin', 'Author']).exists()):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('blog:home')
    
    # Get comments that need moderation or all comments
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        comments = Comment.objects.all().order_by('-created_at')
    else:
        # Authors see comments on their own posts
        comments = Comment.objects.filter(post__author=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/comment_moderation.html', {
        'comments': page_obj,
        'page_obj': page_obj,
    })
