from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from users.models import CustomUser
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from taggit.models import Tag
from .models import Post
from .forms import CommentForm, SearchForm


def home(request):
    return render(
        request,
        'blog/home.html',
    )


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-publish']
    paginate_by = 4

    def get_queryset(self):
        return Post.published.all()

    def get_template_names(self):
        if self.request.path == reverse('home'):
            return 'blog/home.html'
        return 'blog/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/draft_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.draft.filter(author=self.request.user)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            CustomUser, username=self.kwargs.get('username')
        )
        return Post.published.filter(author=user).order_by('-publish')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['author'] = self.object.author
    #     return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    comments = post.comments.filter(active=True)
    form = CommentForm()

    # if request.user != post.author and post.status != Post.Status.DRAFT:
    #     return Http404("This post is not published.")

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
    model = Post
    fields = ['title', 'content', 'post_image', 'tags']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        status = self.request.POST.get('status', 'DF')
        if status not in dict(Post.Status.choices):
            status = 'DF'
        form.instance.status = status
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.status == 'DF':
            return reverse_lazy('blog:draft-list')
        return reverse_lazy('blog:post-detail', kwargs={'slug': self.object.slug})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # To prevent users from updating other people's posts
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')


@require_POST
def post_comment(request, post_id):
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
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def liked_post(request):
    liked_posts = Post.published.filter(users_like=request.user)
    return render(
        request,
        'blog/readinglist.html',
        {'liked_posts': liked_posts}
    )


def tag(request, tag_slug=None):
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
