from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from main.models import Post, Profile
from main.decorators import PostAuthorTest,AjaxTest


class PostGeneralView():
    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user})


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    template_name='post/details.html'
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['is_read'] = self.get_object().read_by_user(self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(PostGeneralView, CreateView):
    template_name = 'post/create.html'
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(PostCreateView, self).form_valid(form)

        subject = 'Новый пост в вашей ленте!'
        message = f'Автор <{self.object.author}> создал новый пост: "{self.object.title}"'
        from_email = "Блог на Django"
        recipient_list = [x[0] for x in list(self.object.author.subscriptions.values_list('email'))]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return response


@method_decorator(login_required, name='dispatch')
class PostUpdateView(PostGeneralView, PostAuthorTest, UpdateView):
    template_name = 'post/update.html'
    model = Post
    fields = ['title', 'content']


@method_decorator(login_required, name='dispatch')
class PostDeleteView(PostGeneralView, PostAuthorTest, DeleteView):
    template_name = 'post/delete.html'
    model = Post

@method_decorator(login_required, name='dispatch')
class PostMarkView(AjaxTest, View):
    template_name = None
    raise_exception = True
    def post(self, *args, **kwargs):
        t = kwargs.get('type')
        post = Post.objects.get(pk=kwargs.get('pk'))
        reader = self.request.user
        if t == 'read':
            post.read_by.add(reader)
            return JsonResponse({"success":True}, status=200)
        elif t == 'unread':
            post.read_by.remove(reader)
            return JsonResponse({"success":True}, status=200)
        else:
            return JsonResponse({"success":False}, status=404)
