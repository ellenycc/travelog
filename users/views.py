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
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile'
    paginate_by = 5

    def get_object(self):
        username = self.kwargs['username']  # Get username from URL
        return get_object_or_404(Profile, user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.user.blog_posts.all()
        return context


@login_required
def settings(request):
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
                request, f'Your account has been updated!'
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
    profile_id = request.POST.get('id')
    action = request.POST.get('action')
    current_user_profile = get_object_or_404(Profile, user=request.user)

    if profile_id and action:
        try:
            # fetch the Profile object with the given id
            profile = Profile.objects.get(id=profile_id)
            # Add the profile to current user profile follows list
            if action == 'follow':
                current_user_profile.follows.add(profile)
            # Remove the profile to current user profile follows list
            else:
                current_user_profile.follows.remove(profile)
            return JsonResponse({'status': 'ok'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
