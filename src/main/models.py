from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Exists
from django.db import models
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from main import image_generators

class Profile(AbstractUser):
    """
        This model is used as DEFAULT user of django project.
        It's used to:
            make relationships with post.author
            manage subscriptions (reverse relationship)
    """
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True
    )
    avatar = ProcessedImageField(
        verbose_name='Profile Avatar'
        upload_to='profiles/',
        processors=[ResizeToFill(100, 100)],
        format='PNG',
        options={'quality': 90},
        null=True, blank=True
    )
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
        """ Get all followers users """
        return self.followers.all()

    def get_following(self):
        """ Get all users that 'self' user is following """
        return self.following.all()

    def is_following(self, target_user):
        """ Checks if 'self.user' is following 'target_user' """
        return target_user.get_followers().filter(pk=self.pk).exists()

    def get_feed(self):
        """ Get all posts that are written by users that 'self.user' is following """
        is_read = Post.objects.filter(
            pk=OuterRef('pk'), read_by__username=self)
        return Post.objects.filter(
            author__in=self.get_following()).order_by('-created_on').annotate(
                is_read=Exists(is_read))

    def get_follow_annotated_profiles(self, queryset):
        """  Returns queryset of annotated profiles: if 'self' user is following or not """
        is_following = Subscription.objects.filter(
            to_profile=self, from_profile=OuterRef('pk'))
        return queryset.annotate(is_following=Exists(is_following))

    def get_related(self):
        """ Get all users except 'self'. They are annotated if followed by 'self' user or not """
        queryset = Profile.objects.exclude(pk=self.pk)
        return self.get_follow_annotated_profiles(queryset).order_by('is_following')

    def get_target_users_followers(self, target_user):
        """
        This method returns all target user followers with annotation
        (whether a 'self' user is following or not)
        Returns Queryset.
        Values: username, is_following
        """
        followers = target_user.get_followers()
        return self.get_follow_annotated_profiles(followers).values('username', 'is_following')

    def get_target_users_following(self, target_user):
        """
        This method returns all target user following with annotation (whether a 'self' user is following or not)
        Returns Queryset.
        Values: username, is_following
        """
        following = target_user.get_following()
        return self.get_follow_annotated_profiles(following).values('is_following', 'username')

    def get_posts(self):
        """ Get all posts where author is a 'self' user"""
        return Post.objects.filter(author=self)


class Subscription(models.Model):
    """
    This class is used to make reverse relationship of Profile model (ManyToMany relationship)
    Basically this class is automatically created by Django.
    This class will be removed in the future updates.
    """    
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
    """
    Good to know:
        Fields:
            read_by - this field is used to check whether users read the post or not
            thumbnail - uses Django-ImageKit module to convert image. Have a look at
                        image_genrators.py and templates/post/post.html files 
                        to see how images made OPTIMIZED
    """
    title = models.CharField(
        verbose_name="Post title",
        max_length=255,
        default='New post'
    )
    content = models.TextField(
        verbose_name="Post content"
    )
    created_on = models.DateTimeField(
        verbose_name="Post created on date",
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='users_read',
        blank=True
    )
    thumbnail = ProcessedImageField(
        verbose_name="Post thumbnail"
        upload_to='posts/',
        format='PNG',
        options={'quality': 100},
        null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']

    def read_by_user(self, user):
        """ Checks whether or not a 'self' post is read by given 'user' """
        return self.read_by.filter(username=user.username).exists()
    
    def getSizes(self):
        """
        Get a touple of sizes.
        It's used on templates only
        Example: (325, 650, 1000)
        """
        return image_generators.sizes
    
    def getFormats(self):
        """
        Get a touple of mime types of image.
        It's used on templates only
        Example: ('png', 'jpeg', 'webp')
        """
        return image_generators.formats
