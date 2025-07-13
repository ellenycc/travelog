"""Views for the blog application.

Handles post listing, detail, creation, editing, comments, likes, and search.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from taggit.models import Tag
from users.models import CustomUser
from .models import Post
from .forms import CommentForm, SearchForm

def home(request):
    """Render the home page."""
    return render(
        request,
        'blog/home.html',
    )

class PostListView(ListView):
    """List view for published blog posts.

    Attributes:
      model: The Post model to display.
      context_object_name: Name for the posts in template context.
      ordering: Default ordering for posts (newest first).
      paginate_by: Number of posts per page.
    """
    model = Post
    context_object_name = 'posts'
    ordering = ['-publish']
    paginate_by = 4

    def get_queryset(self):
        """Return queryset of published posts only."""
        return Post.published.all()

    def get_template_names(self):
        """Return template name based on URL path."""
        if self.request.path == reverse('home'):
            return 'blog/home.html'
        return 'blog/posts.html'

    def get_context_data(self, **kwargs):
        """Add users and tags to context.

        Args:
          **kwargs: Additional context data.

        Returns:
          dict: Context data including users and tags.
        """
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class DraftListView(LoginRequiredMixin, ListView):
    """List view for draft posts of the current user.

    Attributes:
      model: The Post model to display.
      template_name: Template to use for rendering.
      context_object_name: Name for the posts in template context.
      ordering: Default ordering for posts (newest first).
    """
    model = Post
    template_name = 'blog/draft_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        """Return queryset of draft posts for the current user only."""
        return Post.draft.filter(author=self.request.user)

class UserPostListView(ListView):
    """List view for published posts by a specific user.

    Attributes:
      model: The Post model to display.
      template_name: Template to use for rendering.
      context_object_name: Name for the posts in template context.
      paginate_by: Number of posts per page.
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Return queryset of published posts by the specified user only."""
        user = get_object_or_404(
            CustomUser, username=self.kwargs.get('username')
        )
        return Post.published.filter(author=user).order_by('-publish')

def post_detail(request, slug):
    """Render the detail page for a single post, including comments and similar posts.

    Args:
      request: The HTTP request object.
      slug: The slug of the post to display.

    Returns:
      HttpResponse: Rendered post detail template.
    """
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]
    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create view for new blog posts.

    Attributes:
      model: The Post model to create.
      fields: Form fields to include.
      template_name: Template to use for rendering.
    """
    model = Post
    fields = ['title', 'content', 'post_image', 'tags']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        """Set author and status, then save the post.

        Args:
          form: The valid form instance.

        Returns:
          HttpResponse: Redirect to success URL.
        """
        form.instance.author = self.request.user
        status = self.request.POST.get('status', 'DF')
        if status not in dict(Post.Status.choices):
            status = 'DF'
        form.instance.status = status
        return super().form_valid(form)

    def get_success_url(self):
        """Return redirect URL after post creation."""
        if self.object.status == 'DF':
            return reverse_lazy('blog:draft-list')
        return reverse_lazy('blog:post-detail', kwargs={'slug': self.object.slug})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update view for existing blog posts.

    Attributes:
      model: The Post model to update.
      fields: Form fields to include.
    """
    model = Post
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        """Set author and save the post.

        Args:
          form: The valid form instance.

        Returns:
          HttpResponse: Redirect to success URL.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Allow only the author to update the post.

        Returns:
          bool: True if user is the author, False otherwise.
        """
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete view for blog posts.

    Attributes:
      model: The Post model to delete.
      success_url: URL to redirect to after successful deletion.
    """
    model = Post
    success_url = '/blog/'

    def test_func(self):
        """Allow only the author to delete the post.

        Returns:
          bool: True if user is the author, False otherwise.
        """
        post = self.get_object()
        return self.request.user == post.author

def about(request):
    """Render the about page."""
    return render(request, 'blog/about.html')

@require_POST
def post_comment(request, post_id):
    """Handle comment submission for a post.

    Args:
      request: The HTTP request object.
      post_id: The ID of the post to comment on.

    Returns:
      HttpResponse: Redirect to post detail or render comment form with errors.
    """
    post = get_object_or_404(
        Post,
        pk=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('blog:post-detail', slug=post.slug)
    return render(
        request,
        'blog/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )

@login_required
@require_POST
def post_like(request):
    """Handle like/unlike actions for posts.

    Args:
      request: The HTTP request object.

    Returns:
      JsonResponse: JSON response indicating success or error.
    """
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.published.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Post.DoesNotExist:  # type: ignore[attr-defined]
            pass
    return JsonResponse({'status': 'error'})

@login_required
def liked_post(request):
    """Render the reading list of posts liked by the current user.

    Args:
      request: The HTTP request object.

    Returns:
      HttpResponse: Rendered reading list template.
    """
    liked_posts = Post.published.filter(users_like=request.user)
    return render(
        request,
        'blog/readinglist.html',
        {'liked_posts': liked_posts}
    )

def tag(request, tag_slug=None):
    """Render posts filtered by tag.

    Args:
      request: The HTTP request object.
      tag_slug: The slug of the tag to filter by.

    Returns:
      HttpResponse: Rendered tag template with filtered posts.
    """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    return render(
        request,
        'blog/tag.html',
        {
            'post_list': post_list,
            'tag': tag
        }
    )

def post_search(request):
    """Search for posts by query string.

    Args:
      request: The HTTP request object.

    Returns:
      HttpResponse: Rendered search template with results.
    """
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (Post.published.annotate(search=SearchVector('title', 'content'),
                                               )
                       .filter(search=query)
                       )
    return render(
        request,
        'blog/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )
