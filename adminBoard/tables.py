from django import shortcuts
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

class ViewCompany(object):
    verbose_name = _("View")
    name = "view"
    icon = "icon-eye-open"
        
    def allowed(self, request, obj):
        return True

class EditCompany(object):
    verbose_name = _("Edit")
    name = "update"
    icon = "icon-pencil"
        
    def allowed(self, request, obj):
        return True
    
class ViewAppliance(object):
    verbose_name = _("View")
    name = "view"
    icon = "icon-eye-open"
        
    def allowed(self, request, obj):
        return True
        
class EditAppliance(object):
    verbose_name = _("Edit")
    name = "update"
    icon = "icon-pencil"
    modal = True
    
    def allowed(self, request, obj):
        return True
    
    
class DeleteAppliance(object):
    verbose_name = _("Delete")
    name = "delete"
    icon = "icon-trash"
    need_confirm = True
        
    def allowed(self, request, obj):
        return True

class TableAddAppliance(object):
    verbose_name = _("Create")
    name = "create"
    icon = "icon-plus"
    modal = True
        
    def allowed(self, request, obj):
        return True

class TableDeleteAppliance(object):
    verbose_name = _("Delete")
    name = "delete"
    icon = "icon-trash"
    classes = "btn-danger"
        
    def allowed(self, request, obj):
        return True
    
class TableViewAppliance(object):
    verbose_name = _("View")
    name = "view"
    icon = "icon-eye-open"
    modal = False
        
    def allowed(self, request, obj):
        return True