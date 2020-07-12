from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Exists, OuterRef,F
from django.db import models
from django.conf import settings
from django import forms

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from main.fields import MyCustomFormImageField
from main import image_generators

class Profile(AbstractUser):
    email = models.EmailField(
        _('email address'), unique=True)
    
    avatar = ProcessedImageField(upload_to='profiles/',
                                    processors=[ResizeToFill(100,100)],
                                    format='PNG',
                                    options={'quality': 90},
                                    null=True, blank=True)

    followers = models.ManyToManyField(
        to='self',
        related_name='following',
        symmetrical=False,
        through='Subscription'
    )

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def is_following(self, user):
        return user.get_followers().filter(pk=self.pk).exists()

    def get_feed(self):
        is_read = Post.objects.filter(
            pk=OuterRef('pk'), read_by__username=self)
        return Post.objects.filter(
            author__in=self.get_following()).order_by('-created_on').annotate(
                is_read=Exists(is_read))

    def get_related(self):
        queryset = Profile.objects.exclude(pk=self.pk)
        return self.get_follow_annotated_profiles(queryset).order_by('is_following')

    def get_follow_annotated_profiles(self, queryset):
        # Returns queryset of annotated profiles: if 'self' user is following or not

        is_following = Subscription.objects.filter(
            to_profile=self, from_profile=OuterRef('pk'))
        return queryset.annotate(is_following=Exists(is_following))

    def get_target_users_followers(self, target_user):
        # This method returns all target user followers with annotation (whether a 'self' user is following or not)
        # Returns Queryset.
        # Values: username, is_following
        followers = target_user.get_followers()
        return self.get_follow_annotated_profiles(followers).values('username', 'is_following')

    def get_target_users_following(self, target_user):
        # This method returns all target user following with annotation (whether a 'self' user is following or not)
        # Returns Queryset.
        # Values: username, is_following
        following = target_user.get_following()
        return self.get_follow_annotated_profiles(following).values('is_following', 'username')
        # return self.get_follow_annotated_profiles(following).values('is_following', username=F('from_profile__username'))

    def get_posts(self):
        return Post.objects.filter(author=self)


class Subscription(models.Model):
    from_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='from_profiles',
        on_delete=models.CASCADE)
    to_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='to_profiles',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s <= %s" % (
            self.from_profile.username, self.to_profile.username)


class Post(models.Model):
    title = models.CharField(max_length=255, default='New post')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='posts')
    read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='users_read', blank=True)

    thumbnail = ProcessedImageField(upload_to='posts/',
                                    format='PNG',
                                    options={'quality': 100},
                                    null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']

    def read_by_user(self, user):
        return self.read_by.filter(username=user.username).exists()
    
    def getSizes(self):
        return image_generators.sizes
    
    def getFormats(self):
        return image_generators.formats
