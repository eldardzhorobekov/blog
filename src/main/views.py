from django.views.generic import ListView


class HomeView(ListView):
    template_name = 'home.html'
    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['n'] = range(3)
        return context


class ProfileView(ListView):
    template_name = 'profile.html'
    def get_queryset(self):
        return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['n'] = range(3)
        return context


class LoginView(ListView):
    template_name = 'login.html'
    def get_queryset(self):
        return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
