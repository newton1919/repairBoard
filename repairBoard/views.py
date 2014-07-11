# -*- coding: utf-8 -*-
from django import shortcuts
from django.utils.safestring import mark_safe
from adminBoard.models import Company, Appliance
from django.utils.translation import ugettext as _

import json

def index(request):
    context = {"role":""}
    company = Company.objects.filter()[0]
    context["company_desc"] = mark_safe(company.desc)
    return shortcuts.render(request, 'index.html', context)

def appliance_index(request, pk):
    context = {"type": pk}
    context["role"] = ""
    objs = Appliance.objects.filter(type = pk)
    context["objs"] = objs
    return shortcuts.render(request, 'admin/appliance/view.html', context)

def gallery(request):
    context = {}
    return shortcuts.render(request, 'gallery.html', context)

def appliance_single_view(request, pk, appliance_id):
    context = {"type": pk}
    context["role"] = ""
    obj = Appliance.objects.get(type = pk, id = appliance_id)
    context["content"] = mark_safe(obj.content)
    context["title"] = obj.title
    return shortcuts.render(request, 'admin/appliance/single_view.html', context)

def company_contact(request):
    context = {"role":""}
    return shortcuts.render(request, 'admin/company_contact.html',context)

def language(request):
    lang = request.GET.get("language", None)
    if lang:
        request.session['django_language'] = lang
        resp = shortcuts.HttpResponse()
        resp.write(json.dumps({'status':True, 'message':""}))
        resp.set_cookie("django_language", lang)
        return resp
    else:
        return shortcuts.HttpResponse(json.dumps({'status':False, 'message':_("please select language")}))