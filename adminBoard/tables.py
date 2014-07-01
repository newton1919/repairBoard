from django import shortcuts
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

class ViewCompany(object):
    verbose_name = "View"
    name = "view"
    icon = "icon-eye-open"
        
    def allowed(self, request, obj):
        return True

class EditCompany(object):
    verbose_name = "Edit"
    name = "update"
    icon = "icon-pencil"
        
    def allowed(self, request, obj):
        return True
    
class ViewTv(object):
    verbose_name = "View"
    name = "view"
    icon = "icon-eye-open"
        
    def allowed(self, request, obj):
        return True
        
class EditTv(object):
    verbose_name = "Edit"
    name = "update"
    icon = "icon-pencil"
        
    def allowed(self, request, obj):
        return True
    
    
class DeleteTv(object):
    verbose_name = "Delete"
    name = "delete"
    icon = "icon-trash"
        
    def allowed(self, request, obj):
        return True

class AddTv(object):
    verbose_name = "Create"
    name = "create"
    icon = "icon-plus"
        
    def allowed(self, request, obj):
        return True

class TableDeleteTv(object):
    verbose_name = "Delete"
    name = "delete"
    icon = "icon-trash"
        
    def allowed(self, request, obj):
        return True