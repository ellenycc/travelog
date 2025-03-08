from django.urls import path
from .views import (
    DraftListView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('drafts/', DraftListView.as_view(), name='draft-list'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('like/', views.post_like, name='like'),
    path('readinglist/', views.liked_post, name='liked-post'),
    path('tag/<slug:tag_slug>/', views.tag, name='tag'),
    path('search/', views.post_search, name='post_search'),
    path('about/', views.about, name='blog-about'),
]
