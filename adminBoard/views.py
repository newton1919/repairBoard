#-*- coding:utf-8 -*-
from django import shortcuts
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as session_login, logout as session_logout
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from datetime import datetime

from .models import Company, Appliance, Appliance_type
from .forms import *
from .tables import *

from common.decorators import login_required, admin_required
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from common.tables import Column
import json,os

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, 
                               widget=forms.TextInput(attrs={"class":"form-control", "data_class":"no-label", "placeholder":_('username')}))
    #email = forms.EmailField()
    password = forms.CharField(max_length=30,
                                widget=forms.PasswordInput(attrs={"class":"form-control", "data_addon":True ,"data_class":"no-label", "placeholder":_('password')}, render_value=False))
    form_action = "/admin/"
    form_id = "login"
    
    
    
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        super(SignupForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        try:
            username=self.cleaned_data['username']
        except:
            raise forms.ValidationError(_("This username must not be None."))
        return username
    
    def clean(self):
        super(SignupForm, self).clean()
        try:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
        except:
            raise forms.ValidationError(_("This username and password must not be None."))
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                session_login(self.request, user)
                # Redirect to a success page.
            else:
                # Return a 'disabled account' error message
                raise forms.ValidationError(_("disabled account"))
        else:
            # Return an 'invalid login' error message.
            print "The password doesnot match the username"
            raise forms.ValidationError(_("The password doesnot match the username"))
        return self.cleaned_data
    
def login(request):
    if request.user.is_superuser:
        return shortcuts.redirect(reverse("admin:index"))
    
    if request.method == 'POST':
        form = SignupForm(request, data = request.POST)
        if form.is_valid(): 
            return shortcuts.redirect(reverse("admin:index"))
        else:
            return shortcuts.render(request, 'admin/login.html', {'form': form})
    else:
        form = SignupForm()
        print form.visible_fields()[0].field.widget.attrs.get("data_class", "")
        return shortcuts.render(request, 'admin/login.html', {'form': form})

def logout(request):
    session_logout(request)
    form = SignupForm()
    return shortcuts.render(request, 'admin/login.html', {'form': form})

@login_required
@admin_required
def index(request):
    return shortcuts.redirect(reverse("admin:company_index"))

'''    
class CompanyUpdate(FormView):
    #model = Company
    form_class = CompanyForm
    success_url = '/thanks/'
    template_name = "admin/edit.html"
    
    
    
    def get_object(self, *args, **kwargs):
        if not hasattr(self, "_object"):
            company_name = self.kwargs['pk']
            self._object = Company.objects.get(name = company_name)
        return self._object
'''
    
@login_required
@admin_required
def company_update(request, pk):
    if request.method == 'POST':
        form = CompanyForm(request, pk, data = request.POST)
        if form.is_valid(): 
            return shortcuts.redirect(reverse("admin:company_index"))
        else:
            context = {"id":pk}
            context["role"] = "admin/"
            context['form'] = form
            return shortcuts.render(request, 'admin/edit.html',context)
    else:
        company = Company.objects.get(id=pk)
        context = {"id":pk}
        initial_data = {"desc": mark_safe(company.desc),
                   "company_name":company.name,
                   "address":company.address,
                   "city":company.city,
                   "country":company.country,
                   "website":company.website,
                   "contact_people":company.contact_people,
                   "telphone":company.telphone,}
        context["role"] = "admin/"
        companyForm = CompanyForm(initial = initial_data)
        context['form'] = companyForm
        return shortcuts.render(request, 'admin/edit.html',context)

@login_required
@admin_required
def company_detail(request, pk):
    company = Company.objects.get(id=pk)
    context = {"desc": mark_safe(company.desc)}
    context["name"] = company.name
    context["role"] = "admin/"
    return shortcuts.render(request, 'admin/detail.html',context)


def get_desc(obj):
    desc = obj.desc
    return desc[:20]+"..."

def company_contact(request):
    context = {"role":"admin/"}
    return shortcuts.render(request, 'admin/company_contact.html',context)

@login_required
@admin_required
def company_index(request):
    #company = Company.objects.get(name=pk)
    #context = {"desc": mark_safe(company.desc)}
    context = {"role":"admin/"}
    name = Column(_("Company") +_("Name"), transform = "name")
    address = Column(_("Address"), transform = "address")
    website = Column(_("Website"), transform = "website")
    desc = Column(_("Description"), transform = get_desc)
    col_list = [name, address, website, desc]
    context["columns"] = col_list
    #get render data
    objs = Company.objects.filter()
    display_values = []
    if objs:
        for obj in objs:
            for col in col_list:
                attr = col.transform
                ajax_tag = col.ajax
                if callable(attr):
                    col_value = {"ajax":ajax_tag,"key":col.name, "value":attr(obj)}
                else:
                    col_value = {"ajax":ajax_tag,"key":col.name, "value":getattr(obj,attr)}
                display_values.append(col_value)
            obj.display_values = display_values
            display_values = []
    
    context["objs"] = objs
    #define row actions
    row_view_action = ViewCompany()
    row_edit_action = EditCompany()
    row_actions = [row_view_action, row_edit_action]
    context["row_actions"] = row_actions
    #end
    return shortcuts.render(request, 'admin/company.html',context)

def get_content(obj):
    content = obj.content
    return content[:10]+"..."

def appliance_index_orig(request):
    context = {"role":"admin/"}
    type_list = Appliance_type.objects.filter()
    if not type_list:
        return shortcuts.render(request, 'admin/appliance/index_none.html',context)
    else:
        return shortcuts.redirect("/admin/appliance/"+str(type_list[0].id)+"/index")
    
@login_required
@admin_required
def appliance_index(request, pk):
    context = {"role":"admin/"}
    appliance_type = Appliance_type.objects.get(id = pk)
    context["type"] = appliance_type.type
    context["type_id"] = pk
    title = Column(_("Title"), transform = "title")
    thumbnail = Column(_("Thumbnail"), transform = "thumbnail")
    content = Column(_("Content"), transform = get_content)
    create_at = Column(_("Create_time"), transform = "create_at")
    #update_at = Column("Update_time", transform = "update_at")
    
    col_list = [title, thumbnail, content, create_at,]
    context["columns"] = col_list
    #get render data
    objs = Appliance.objects.filter(type = appliance_type.type)
    display_values = []
    if objs:
        for obj in objs:
            for col in col_list:
                attr = col.transform
                ajax_tag = col.ajax
                if callable(attr):
                    col_value = {"ajax":ajax_tag,"key":col.name, "value":attr(obj)}
                else:
                    col_value = {"ajax":ajax_tag,"key":col.name, "value":getattr(obj,attr)}
                display_values.append(col_value)
            obj.display_values = display_values
            display_values = []
    
    context["objs"] = objs
    #define row actions
    row_view_action = ViewAppliance()
    row_edit_action = EditAppliance()
    row_delete_action = DeleteAppliance()
    row_actions = [row_view_action, row_edit_action, row_delete_action]
    context["row_actions"] = row_actions
    #end
    #define table actions
    table_view_action = TableViewAppliance()
    table_add_action = TableAddAppliance()
    table_delete_action = TableDeleteAppliance()
    table_actions = [table_view_action, table_add_action, table_delete_action,]
    context["table_actions"] = table_actions
    #end
    return shortcuts.render(request, 'admin/appliance/index.html',context)
            
@login_required
@admin_required
def appliance_create(request, pk):
    appliance_type = Appliance_type.objects.get(id = pk)
    type2 = appliance_type.type
    print type2
    if request.method == 'POST':
        form = ApplianceCreateForm(request, pk, type2, data = request.POST)
        if form.is_valid(): 
            return shortcuts.redirect("/admin/appliance/"+pk+"/index")
        else:
            context = {"type_id": pk, "type": type2}
            context["role"] = "admin/"
            context['form'] = form
            return shortcuts.render(request, 'admin/appliance/create.html', context)
        ###end 
    else:
        context = {"type_id": pk, "type": type2}
        context["role"] = "admin/"
        context["form"] = ApplianceCreateForm()
        return shortcuts.render(request, 'admin/appliance/create.html', context)

@login_required
@admin_required
def appliance_type_create(request):
    if request.method == 'POST':
        form = ApplianceTypeForm(request, data = request.POST)
        if form.is_valid(): 
            return shortcuts.redirect(reverse("admin:appliance_index_orig"))
        else:
            context = {}
            context["role"] = "admin/"
            context["form"] = form
            return shortcuts.render(request, 'admin/appliance/type_create.html', context)
    else:
        form = ApplianceTypeForm()
        context = {}
        context["role"] = "admin/"
        context["form"] = form
        return shortcuts.render(request, 'admin/appliance/type_create.html', context)

@login_required
@admin_required
def appliance_type_delete(request, type_id):
    appliance_type = Appliance_type.objects.get(id = type_id)
    type2 = appliance_type.type
    appliance_type.delete()
    
    Appliance.objects.filter(type = type2).delete()
    return shortcuts.redirect(reverse("admin:appliance_index_orig"))
    
def appliance_view(request, pk):
    appliance_type = Appliance_type.objects.get(id = pk)
    type2 = appliance_type.type
    
    context = {"type": type2}
    context["type_id"] = pk
    context["role"] = "admin/"
    objs = Appliance.objects.filter(type = type2)
    context["objs"] = objs
    return shortcuts.render(request, 'admin/appliance/view.html', context)

def appliance_single_view(request, pk, appliance_id):
    appliance_type = Appliance_type.objects.get(id = pk)
    type2 = appliance_type.type
    
    context = {"type": type2}
    context["type_id"] = pk
    context["role"] = "admin/"
    obj = Appliance.objects.get(type = type2, id = appliance_id)
    context["content"] = mark_safe(obj.content)
    context["title"] = obj.title
    return shortcuts.render(request, 'admin/appliance/single_view.html', context)

@login_required
@admin_required
def appliance_single_delete(request, pk, appliance_id):
    appliance_type = Appliance_type.objects.get(id = pk)
    type2 = appliance_type.type
    
    context = {"type": type2}
    context["type_id"] = pk
    context["role"] = "admin/"
    obj = Appliance.objects.get(type = type2, id = appliance_id)
    static_path = obj.thumbnail
    thumbnail_name = os.path.basename(static_path)
    thumbnail_path = os.path.join(settings.BASE_DIR, "static", "images/thumbnails", type2, thumbnail_name)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    #删除对应的缩略图
    obj.delete()
    
    return shortcuts.redirect("/admin/appliance/"+pk+"/index")

@login_required
@admin_required
def appliance_single_update(request, pk, appliance_id):
    appliance_type = Appliance_type.objects.get(id = pk)
    type2 = appliance_type.type
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        thumbnails = request.FILES.get('thumbnail', "")
        if not thumbnails:
            #缩略图没有改变
            thumbnail_after = ""
        else:
            #缩略图改变
            thumbnail = thumbnails
            thumbnail_after = handle_uploaded_file(thumbnail, type2)
            #删除原来的缩略图
            current_appliance = Appliance.objects.get(id = appliance_id)
            static_path = current_appliance.thumbnail
            thumbnail_name = os.path.basename(static_path)
            thumbnail_path = os.path.join(settings.BASE_DIR, "static", "images/thumbnails", type2, thumbnail_name)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
        #update table Appliance
        try:
            update_at = datetime.now()
            current_appliance = Appliance.objects.get(id = appliance_id)
            current_appliance.title = title
            current_appliance.content = content
            current_appliance.update_at = update_at
            if thumbnail_after:
                current_appliance.thumbnail = thumbnail_after
            current_appliance.save()
            return shortcuts.HttpResponse(json.dumps({'status':True, 'message':""}))
        except Exception,e:
            return shortcuts.HttpResponse(json.dumps({'status':False, 'message':e.message}))
    else:
        appliance = Appliance.objects.get(id = appliance_id)
        context = {"type_id": pk, "type": type2}
        context["appliance_id"] = appliance_id
        context["role"] = "admin/"
        context["title"] = appliance.title
        context["content"] = mark_safe(appliance.content)
        context["thumbnail_path"] = appliance.thumbnail
        return shortcuts.render(request, 'admin/appliance/update.html', context)