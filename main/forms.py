from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('date_time_start', 'date_time_end', 'description', 'category', 'reservation', 'on_main')
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Описание'}),
        }