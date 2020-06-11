from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from main.models import Post, Profile
from main.decorators import PostTest

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['posts'] = user.get_feed()
        context['follow_list'] = user.get_related().values('username', 'is_following')
        return context


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
class PostDetailView(DetailView):
    template_name='post/details.html'
    model = Post


class PostGeneralView():
    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user})


@method_decorator(login_required, name='dispatch')
class PostCreateView(PostGeneralView, CreateView):
    template_name = 'post/create.html'
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(PostGeneralView, PostTest, UpdateView):
    template_name = 'post/update.html'
    model = Post
    fields = ['title', 'content']


@method_decorator(login_required, name='dispatch')
class PostDeleteView(PostGeneralView, PostTest, DeleteView):
    template_name = 'post/delete.html'
    model = Post


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
