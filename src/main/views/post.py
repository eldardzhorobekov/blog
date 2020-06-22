from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from main.models import Post
from main.decorators import PostAuthorTest, AjaxTest


class PostGeneralView():

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user})


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    template_name = 'post/details.html'
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

        message = 'Автор <%s> создал новый пост: %s' % (
            self.object.author, self.objects.title)
        from_email = settings.EMAIL_HOST_USER
        recievers = self.object.author.subscriptions.values_list(
            'email', flat=True)
        if recievers.count() > 0:
            send_mail(
                subject, message, from_email, recievers, fail_silently=True
            )
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
            return JsonResponse({"success": True}, status=200)
        elif t == 'unread':
            post.read_by.remove(reader)
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=404)
