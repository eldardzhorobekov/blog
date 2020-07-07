from django import forms
from main.models import Post
from main.fields import MyCustomImageField


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'thumbnail')
        widgets = {
            'content': forms.TextInput(attrs={'class': 'materialize-textarea'}),
        }
        field_classes = {
            'thumbnail': MyCustomImageField,
        }

