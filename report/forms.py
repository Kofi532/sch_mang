from django import forms
from .models import report

class ReportForm(forms.ModelForm):

    class Meta:
        model = report
        fields = ['subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL']




#['stu_id', 'subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL', 'school']
