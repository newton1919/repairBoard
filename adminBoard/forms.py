#-*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.conf import settings
from .models import Company, Appliance, Appliance_type
from datetime import datetime
import os

def handle_uploaded_file(f, pk):
    upload_path = os.path.join(settings.BASE_DIR, "django-summernote", "images/thumbnails", pk)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    with open(os.path.join(upload_path, str(f)), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join("/media/images/thumbnails", pk, str(f))

class ApplianceCreateForm(forms.Form):
    input_title = forms.CharField(max_length=60, required=True, label = _('Title'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Title')}))
    #thumbnail = forms.FileField(required=False)
    content = forms.CharField(initial=_("Title"),
                              widget=SummernoteWidget())
    
    def __init__(self, request=None, pk=None, type2=None, *args, **kwargs):
        self.request = request
        self.pk = pk
        self.type2 = type2
        super(ApplianceCreateForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(ApplianceCreateForm, self).clean()
        try:
            title = self.cleaned_data['input_title']
            content = self.cleaned_data['content']
            thumbnails = self.request.FILES.get('thumbnail', "")
            if not thumbnails:
                thumbnail_after = ""
            else:
                thumbnail = thumbnails
                thumbnail_after = handle_uploaded_file(thumbnail, self.type2)
            #store into table Appliance
            create_at = datetime.now()
            appliance_obj = Appliance(type=self.type2, title=title, thumbnail=thumbnail_after, content=content, create_at=create_at, update_at=create_at)
            appliance_obj.save()

        except Exception, e:
            print e.message
            raise forms.ValidationError(_(e.message))
        return self.cleaned_data

class ApplianceUpdateForm(forms.Form):
    input_title = forms.CharField(max_length=60, required=True, label = _('Title'),
                               widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_('Title')}))
    #thumbnail = forms.FileField(required=False)
    content = forms.CharField(widget=SummernoteWidget())
    
    def __init__(self, request=None, pk=None, type2=None, appliance_id=None, *args, **kwargs):
        self.request = request
        self.pk = pk
        self.type2 = type2
        self.appliance_id = appliance_id
        super(ApplianceUpdateForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(ApplianceUpdateForm, self).clean()
        try:
            title = self.cleaned_data['input_title']
            content = self.cleaned_data['content']
            thumbnails = self.request.FILES.get('thumbnail', "")
            if not thumbnails:
                #缩略图没有改变
                thumbnail_after = ""
            else:
                #缩略图改变
                thumbnail = thumbnails
                thumbnail_after = handle_uploaded_file(thumbnail, self.type2)
                #删除原来的缩略图
                current_appliance = Appliance.objects.get(id = self.appliance_id)
                static_path = current_appliance.thumbnail
                thumbnail_name = os.path.basename(static_path)
                thumbnail_path = os.path.join(settings.BASE_DIR, "django-summernote", "images/thumbnails", self.type2, thumbnail_name)
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
            #update table Appliance
            update_at = datetime.now()
            current_appliance = Appliance.objects.get(id = self.appliance_id)
            current_appliance.title = title
            current_appliance.content = content
            current_appliance.update_at = update_at
            if thumbnail_after:
                current_appliance.thumbnail = thumbnail_after
            current_appliance.save()

        except Exception, e:
            print e.message
            raise forms.ValidationError(_(e.message))
        return self.cleaned_data
    
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