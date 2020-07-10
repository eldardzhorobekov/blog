from django import forms

from main.models import Post, Profile
from main.fields import MyCustomFormImageField


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'thumbnail')
        widgets = {
            'content': forms.TextInput(attrs={'class': 'materialize-textarea'}),
        }
        field_classes = {
            'thumbnail': MyCustomFormImageField,
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'email',
            'first_name',
            'last_name'
        )