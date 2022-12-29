from django import forms
from .models import reportn

class ReportForm(forms.ModelForm):

    class Meta:
        model = reportn
        fields = ['subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL']




#['stu_id', 'subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL', 'school']
