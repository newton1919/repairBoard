from django import forms
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Company, Appliance, Appliance_type

class CompanyForm(forms.Form):
    company_name = forms.CharField(max_length=60, required=True, label = _('Name'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Name')}))
    country = forms.CharField(max_length=20, required=False, label = _('Country'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Country')}))
    city = forms.CharField(max_length=20, required=False, label = _('City'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('City')}))
    address = forms.CharField(max_length=60, required=True, label = _('Address'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Address')}))
    website = forms.CharField(max_length=60, required=False, label = _('Website'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Website')}))
    contact_people = forms.CharField(max_length=60, required=False, label = _('Contact people'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Contact people')}))
    telphone = forms.CharField(max_length=60, required=False, label = _('Telphone'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Telphone')}))
    
    desc = forms.CharField(widget=SummernoteWidget())
    form_id = "company_edit"
    def __init__(self, request=None, pk=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.pk = pk
        super(CompanyForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(CompanyForm, self).clean()
        
        desc = self.cleaned_data['desc']
        name = self.cleaned_data['company_name']
        address = self.cleaned_data['address']
        city = self.cleaned_data['city']
        country = self.cleaned_data['country']
        website = self.cleaned_data['website']
        contact_people = self.cleaned_data['contact_people']
        telphone = self.cleaned_data['telphone']
        try:
            company = Company.objects.get(id=self.pk)
            company.desc = desc
            company.name = name
            company.address = address
            company.city = city
            company.country = country
            company.website = website
            company.contact_people = contact_people
            company.telphone = telphone
            company.save()
        except Exception, e:
            raise forms.ValidationError(_(e.message))
        return self.cleaned_data
    
class ApplianceTypeForm(forms.Form):
    type = forms.CharField(max_length=20, required=True, label=_("Type"),
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    desc = forms.CharField(max_length=80, required=False, label=_("Description"), 
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    
    form_id = "appliance_type"
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