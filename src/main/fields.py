from django import forms

class MyCustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'fields/my_custom_clearable_file_input.html'

    def get_context(self, name, value, attrs):
        context = super(MyCustomClearableFileInput, self).get_context(name, value, attrs)
        context['widget']['image_class'] = 'my_custom_image_field_class' # you must specify this class
        return context


class MyCustomImageField(forms.ImageField):
    widget = MyCustomClearableFileInput