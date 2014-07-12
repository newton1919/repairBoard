from django import forms
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Company, Appliance, Appliance_type

class CompanyForm(forms.Form):
    name = forms.CharField()
    desc = forms.CharField(widget=SummernoteWidget())
    
class ApplianceTypeForm(forms.Form):
    type = forms.CharField(max_length=20, required=True, label=_("Type"),
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    desc = forms.CharField(max_length=80, required=False, label=_("Description"), 
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        super(ApplianceTypeForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        super(ApplianceTypeForm, self).clean()
        try:
            type = self.cleaned_data['type']
            desc = self.cleaned_data['desc']
        except:
            raise forms.ValidationError("This type and desc must not be None.")
        #store into db
        appliance_type = Appliance_type(type = type, desc = desc)
        appliance_type.save()
        
        return self.cleaned_data