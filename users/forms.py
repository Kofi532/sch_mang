from django import forms
from .models import use

class PostForm(forms.ModelForm):

    class Meta:
        model = use
        fields = ['username']

