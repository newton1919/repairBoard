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

from .models import Company
from .forms import CompanyForm

from common.decorators import login_required, admin_required
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

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

class IndexView(ListView):
    model = Company
    template_name = "admin/company.html"

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
            company = Company.objects.get(name=pk)
            company.desc = desc
            company.save()
            return shortcuts.HttpResponse(json.dumps({'status':True, 'message':""}))
        except:
            return shortcuts.HttpResponse(json.dumps({'status':False, 'message':""}))
    else:
        company = Company.objects.get(name=pk)
        context = {"desc": mark_safe(company.desc)}
        return shortcuts.render(request, 'admin/edit.html',context)

@login_required
@admin_required
def company_detail(request, pk):
    company = Company.objects.get(name=pk)
    context = {"desc": mark_safe(company.desc)}
    return shortcuts.render(request, 'admin/detail.html',context)
    