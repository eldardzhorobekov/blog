from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from main.models import Post, Profile


class IsAuthorOfPostTest(UserPassesTestMixin):

    def test_func(self):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        return self.request.user.is_authenticated and post.author == self.request.user

    def handle_no_permission(self):
        return redirect('post-details', pk=self.kwargs.get('pk'))


class AuthenticationTest(UserPassesTestMixin):

    def test_func(self):
        requested_user = Profile.objects.get(username=self.kwargs.get('username'))
        return self.request.user.is_authenticated and requested_user == self.request.user

    def handle_no_permission(self):
        return redirect('profile', username=self.kwargs.get('username'))


class AjaxTest(UserPassesTestMixin):

    def test_func(self):
        return self.request.is_ajax()

    def handle_no_permission(self):
        return redirect('home')
