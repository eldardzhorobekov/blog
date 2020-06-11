
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Exists, OuterRef
from django.db import models
from django.conf import settings

# Create your models here.


class Profile(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    subscriptions = models.ManyToManyField(
        to='self',
        related_name='followers',
        symmetrical=False,
        through='Subscription'
    )

    def __str__(self):
        return self.username
    def __unicode__(self):
        return self.username

    def get_followers(self):
        return self.subscriptions.filter(to_profiles__from_profile=self)

    def get_following(self):
        return self.subscriptions.filter(from_profiles__to_profile=self)

    def is_following(self, user):
        return Subscription.objects.filter(to_profile=self, from_profile=user).exists()

    def get_feed(self):
        is_read = Post.objects.filter(pk=OuterRef('pk'), read_by__username=self)
        return Post.objects.filter(author__in=self.get_following()).order_by('-created_on').annotate(is_read=Exists(is_read))

    def get_related(self):
        is_following = Exists(Subscription.objects.filter(to_profile=self, from_profile=OuterRef('pk')))
        return Profile.objects.exclude(pk=self.pk).annotate(is_following = is_following)

    def get_posts(self):
        return Post.objects.filter(author=self)

class Subscription(models.Model):
    from_profile = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_profiles', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_profiles', on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, default="New post", null=False)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_read', blank=True, null=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_on']
    def read_by_user(self, user):
        return self.read_by.filter(username=user.username).exists()