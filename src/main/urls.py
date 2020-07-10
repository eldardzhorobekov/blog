from django.urls import path, re_path
from . import views


urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),
     path('profile/<username>', views.ProfileView.as_view(), name='profile'),
     path('profile/<slug>/edit', views.ProfileEditView.as_view(), name='profile-edit'),
     path('profile/<username>/<follow>', views.ProfileFollowView.as_view(), name='profile-follow'),
     path('login', views.LoginView.as_view(), name='login'),
     path('logout', views.logout_view, name='logout'),
     path('post/create', views.PostCreateView.as_view(), name='post-create'),
     path('post/<int:pk>', views.PostDetailView.as_view(), name='post-details'),
     path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
     path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
     path('post/<int:pk>/mark-<type>', views.PostMarkView.as_view(), name='post-mark-as-read'),
]
