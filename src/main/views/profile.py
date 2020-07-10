from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from django.urls import reverse

from main.models import Profile
from main.decorators import AjaxTest, AuthenticationTest


@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    template_name = 'profile/profile.html'
    model = Profile
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = kwargs.get('object')
        context['followers_cnt'] = profile.get_followers().count()
        context['following_cnt'] = profile.get_following().count()
        context['posts'] = profile.get_posts()
        context['is_following'] = self.request.user.is_following(profile)
        return context


@method_decorator(login_required, name='dispatch')
class ProfileEditView(AuthenticationTest, UpdateView):
    template_name = "profile/profile-edit.html"
    model = Profile
    fields = ['first_name', 'last_name', 'email']
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'slug'
    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user})


@method_decorator(login_required, name='dispatch')
class ProfileFollowView(AjaxTest, View):
    template_name = None
    raise_exception = True

    def post(self, *args, **kwargs):
        t = kwargs.get('follow')
        author = Profile.objects.get(username=kwargs.get('username'))
        follower = self.request.user
        if t == 'follow':
            author.subscriptions.add(follower)
            return JsonResponse({"success": True}, status=200)
        elif t == 'unfollow':
            author.subscriptions.remove(follower)
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=404)


class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
