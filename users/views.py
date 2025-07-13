"""Views for user registration, profile management, and user settings.

Handles registration, profile display, settings, and follow actions.
"""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_POST

from blog.models import Post
from users.models import CustomUser, Profile
from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileUpdateForm

def register(request):
    """Handle user registration form and account creation.

    Args:
      request: The HTTP request object.

    Returns:
      HttpResponse: Rendered registration form or redirect to login.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})

class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a user's profile page.

    Attributes:
      model: The Profile model to display.
      template_name: Template to use for rendering.
      context_object_name: Name for the profile in template context.
      paginate_by: Number of posts per page.
    """
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile'
    paginate_by = 5

    def get_object(self, queryset=None):
        """Return the profile object for the given username.

        Returns:
          Profile: The profile object for the specified username.
        """
        username = self.kwargs['username']
        return get_object_or_404(Profile, user__username=username)

    def get_context_data(self, **kwargs):
        """Add the user's posts to the context.

        Args:
          **kwargs: Additional context data.

        Returns:
          dict: Context data including user's posts.
        """
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.user.blog_posts.all()
        return context

@login_required
def settings(request):
    """Allow users to update their account and profile information.

    Args:
      request: The HTTP request object.

    Returns:
      HttpResponse: Rendered settings form or redirect to profile.
    """
    if request.method == 'POST':
        u_form = CustomUserChangeForm(data=request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, 'Your account has been updated!'
            )
        return redirect('profile', username=request.user.username)
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/settings.html', context)

@require_POST
@login_required
def follow(request):
    """Handle follow/unfollow actions for user profiles.

    Args:
      request: The HTTP request object.

    Returns:
      JsonResponse: JSON response indicating success or error.
    """
    profile_id = request.POST.get('id')
    action = request.POST.get('action')
    current_user_profile = get_object_or_404(Profile, user=request.user)
    if profile_id and action:
        try:
            profile = Profile.objects.get(id=profile_id)  # type: ignore[attr-defined]
            if action == 'follow':
                current_user_profile.follows.add(profile)
            else:
                current_user_profile.follows.remove(profile)
            return JsonResponse({'status': 'ok'})
        except Profile.DoesNotExist:  # type: ignore[attr-defined]
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
