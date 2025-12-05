"""
URL configuration for blog app.
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post list
    path('', views.PostListView.as_view(), name='home'),
    
    # Category and tag filtering
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag_posts'),
    
    # Author dashboard and CRUD (must come before detail view to avoid conflicts)
    path('dashboard/', views.AuthorDashboardView.as_view(), name='dashboard'),
    path('post/create/', views.CreatePostView.as_view(), name='post_create'),
    
    # Comments (must come before detail view)
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/moderation/', views.comment_moderation, name='comment_moderation'),
    
    # Post edit and delete (must come before detail view)
    path('post/<slug:slug>/edit/', views.UpdatePostView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.DeletePostView.as_view(), name='post_delete'),
    
    # Post detail (must be last to avoid matching other patterns)
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]

