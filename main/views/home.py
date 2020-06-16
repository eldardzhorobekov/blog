from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from main.models import Post, Profile


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