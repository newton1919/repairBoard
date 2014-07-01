#-*- coding:utf-8 -*-
from django import shortcuts
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as session_login, logout as session_logout
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe

from .models import Company, Appliance
from .forms import CompanyForm
from .tables import *

from common.decorators import login_required, admin_required
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from common.tables import Column
import json
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
        return shortcuts.render(request, 'admin/edit.html',context)

@login_required
@admin_required
def company_detail(request, pk):
    company = Company.objects.get(id=pk)
    context = {"desc": mark_safe(company.desc)}
    return shortcuts.render(request, 'admin/detail.html',context)


def get_desc(obj):
    desc = obj.desc
    return desc[:20]+"..."

@login_required
@admin_required
def company_index(request):
    #company = Company.objects.get(name=pk)
    #context = {"desc": mark_safe(company.desc)}
    context = {}
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
    return ""

@login_required
@admin_required
def appliance_index(request, pk):
    #company = Company.objects.get(name=pk)
    #context = {"desc": mark_safe(company.desc)}
    context = {}
    context["type"] = pk
    title = Column("Title", transform = "title")
    thumbnail = Column("Thumbnail", transform = "thumbnail")
    content = Column("Content", transform = get_content)
    create_at = Column("Create_time", transform = "create_at")
    update_at = Column("Update_time", transform = "update_at")
    
    col_list = [title, thumbnail, content, create_at, update_at]
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
    row_view_action = ViewTv()
    row_edit_action = EditTv()
    row_delete_action = DeleteTv()
    row_actions = [row_view_action, row_edit_action, row_delete_action]
    context["row_actions"] = row_actions
    #end
    #define table actions
    table_add_action = AddTv()
    table_delete_action = TableDeleteTv()
    table_actions = [table_add_action, table_delete_action,]
    context["table_actions"] = table_actions
    #end
    return shortcuts.render(request, 'admin/appliance/index.html',context)
    
@login_required
@admin_required
def appliance_create(request, pk):
    context = {}
    return shortcuts.render(request, 'admin/appliance/create.html', context)