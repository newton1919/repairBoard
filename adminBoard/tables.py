from django import shortcuts
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

class ViewCompany(object):
    verbose_name = "View"
    name = "view"
    icon = "icon-eye-open"
        
    def allowed(self, request, obj):
        return True
    @staticmethod    
    def action(request, obj_id):
        return shortcuts.redirect("/admin/company/saiway/detail")
    
class EditCompany(object):
    verbose_name = "Edit"
    name = "update"
    icon = "icon-pencil"
        
    def allowed(self, request, obj):
        return True
    @staticmethod    
    def action(request, obj_id):
        return shortcuts.redirect("/admin/company/saiway/update")