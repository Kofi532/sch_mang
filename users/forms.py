from django import forms
from .models import use, sch_reg, act, class_fee

class PostForm(forms.ModelForm):

    class Meta:
        model = use
        fields = ['username']

class RegForm(forms.ModelForm):

    class Meta:
        model = sch_reg
        fields = ['full_sch', 'contact_details']

class ActTerm(forms.ModelForm):

    class Meta:
        model = act
        fields = ['active_term']

class FeeForm(forms.ModelForm):
    class Meta:
        model = class_fee
        fields = ['classes', 'fee']