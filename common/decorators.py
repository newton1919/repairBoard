from django import shortcuts
from django.http import HttpResponse
import json

def login_required(method):
    def wrapper(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated():
            #not login
            return shortcuts.redirect("/admin/")
        else:
            #already login
            return method(request, *args, **kwargs)
    return wrapper

def admin_required(method):
    def wrapper(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_superuser:
            #not admin
            return HttpResponse(json.dumps({'status':False, 'message':"only admin permitted with this action"}),status=200)
        else:
            #is admin
            return method(request, *args, **kwargs)
    return wrapper