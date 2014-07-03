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
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    #email = forms.EmailField()
    password = forms.CharField(max_length=30,
                                widget=forms.PasswordInput(attrs={"class":"form-control"}, render_value=False))
    form_action = "/admin/"
    
    
    
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
            raise forms.ValidationError("This username must not be None.")
        return username
    
    def clean(self):
        super(SignupForm, self).clean()
        try:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
        except:
            raise forms.ValidationError("This username and password must not be None.")
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                session_login(self.request, user)
                # Redirect to a success page.
            else:
                # Return a 'disabled account' error message
                raise forms.ValidationError("disabled account")
        else:
            # Return an 'invalid login' error message.
            print "The password doesnot match the username"
            raise forms.ValidationError("The password doesnot match the username")
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
        desc = request.POST.get("desc", None)
        #print desc,pk
        #store to db
        try:
            company = Company.objects.get(id=pk)
            company.desc = desc
            company.save()
            return shortcuts.HttpResponse(json.dumps({'status':True, 'message':""}))
        except:
            return shortcuts.HttpResponse(json.dumps({'status':False, 'message':""}))
    else:
        company = Company.objects.get(id=pk)
        context = {"desc": mark_safe(company.desc), "id":pk}
        context["role"] = "admin/"
        return shortcuts.render(request, 'admin/edit.html',context)

@login_required
@admin_required
def company_detail(request, pk):
    company = Company.objects.get(id=pk)
    context = {"desc": mark_safe(company.desc)}
    context["role"] = "admin/"
    return shortcuts.render(request, 'admin/detail.html',context)


def get_desc(obj):
    desc = obj.desc
    return desc[:20]+"..."

@login_required
@admin_required
def company_index(request):
    #company = Company.objects.get(name=pk)
    #context = {"desc": mark_safe(company.desc)}
    context = {"role":"admin/"}
    name = Column("Company Name", transform = "name")
    address = Column("Address", transform = "address")
    website = Column("Website", transform = "website")
    desc = Column("Description", transform = get_desc)
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
        return shortcuts.redirect("/admin/appliance/"+type_list[0].type+"/index")
    
@login_required
@admin_required
def appliance_index(request, pk):
    #company = Company.objects.get(name=pk)
    #context = {"desc": mark_safe(company.desc)}
    context = {"role":"admin/"}
    context["type"] = pk
    title = Column("Title", transform = "title")
    thumbnail = Column("Thumbnail", transform = "thumbnail")
    content = Column("Content", transform = get_content)
    create_at = Column("Create_time", transform = "create_at")
    #update_at = Column("Update_time", transform = "update_at")
    
    col_list = [title, thumbnail, content, create_at,]
    context["columns"] = col_list
    #get render data
    objs = Appliance.objects.filter(type = pk)
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

def handle_uploaded_file(f, pk):
    upload_path = os.path.join(settings.BASE_DIR, "static", "images/thumbnails", pk)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    with open(os.path.join(upload_path, str(f)), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join("/static/images/thumbnails", pk, str(f))
            
@login_required
@admin_required
def appliance_create(request, pk):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        thumbnails = request.FILES.get('thumbnail', "")
        if not thumbnails:
            thumbnail_after = ""
        else:
            thumbnail = thumbnails
            thumbnail_after = handle_uploaded_file(thumbnail, pk)
        #store into table Appliance
        create_at = datetime.now()
        appliance_obj = Appliance(type=pk, title=title, thumbnail=thumbnail_after, content=content, create_at=create_at, update_at=create_at)
        appliance_obj.save()
            
        return shortcuts.HttpResponse(json.dumps({'status':True, 'message':""}))
    else:
        context = {"type": pk}
        context["role"] = "admin/"
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

    
def appliance_view(request, pk):
    context = {"type": pk}
    context["role"] = "admin/"
    objs = Appliance.objects.filter(type = pk)
    context["objs"] = objs
    return shortcuts.render(request, 'admin/appliance/view.html', context)

def appliance_single_view(request, pk, appliance_id):
    context = {"type": pk}
    context["role"] = "admin/"
    obj = Appliance.objects.get(type = pk, id = appliance_id)
    context["content"] = mark_safe(obj.content)
    context["title"] = obj.title
    return shortcuts.render(request, 'admin/appliance/single_view.html', context)

@login_required
@admin_required
def appliance_single_delete(request, pk, appliance_id):
    context = {"type": pk}
    context["role"] = "admin/"
    obj = Appliance.objects.get(type = pk, id = appliance_id)
    static_path = obj.thumbnail
    thumbnail_name = os.path.basename(static_path)
    thumbnail_path = os.path.join(settings.BASE_DIR, "static", "images/thumbnails", pk, thumbnail_name)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    #删除对应的缩略图
    obj.delete()
    
    return shortcuts.redirect("/admin/appliance/"+pk+"/index")