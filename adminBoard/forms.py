from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CompanyForm(forms.Form):
    name = forms.CharField()
    desc = forms.CharField(widget=SummernoteWidget())