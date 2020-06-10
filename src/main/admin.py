from django.contrib import admin
from .models import Profile, Post
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class SubscribeInline(admin.TabularInline):
    model = Profile.subscriptions.through
    fk_name = 'from_profile'
    extra = 0


class FollowInline(admin.TabularInline):
    model = Profile.subscriptions.through
    fk_name = 'to_profile'
    extra = 0


class ProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    inlines = [SubscribeInline,FollowInline]

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    fieldsets = (
        (None, {'fields': ('title', 'content', 'author')}),
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
