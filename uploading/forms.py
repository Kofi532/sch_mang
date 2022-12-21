from django import forms
from .models import sch_name

class PostForm(forms.ModelForm):

    class Meta:
        model = sch_name
        fields = ['Full_School_Name']
