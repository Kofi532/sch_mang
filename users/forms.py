from django import forms
from .models import use, sch_reg

class PostForm(forms.ModelForm):

    class Meta:
        model = use
        fields = ['username']

class RegForm(forms.ModelForm):

    class Meta:
        model = sch_reg
        fields = ['full_sch', 'contact_details']
