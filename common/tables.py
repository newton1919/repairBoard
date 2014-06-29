from django import shortcuts


class Column(object):
    def __init__(self, verbose_name, transform = None ,ajax = False):
        self.ajax = ajax
        self.verbose_name = verbose_name
        if callable(transform):
            self.transform = transform
            self.name = "<%s callable>" % transform.__name__
        else:
            self.transform = unicode(transform)
            self.name = self.transform
            

    
class StartInstance(object):
    verbose_name = "Start"
    name = "start"

    def allowed(self, request, instance):
        return instance.status in ("SHUTDOWN", "SHUTOFF", "CRASHED")
    
    @staticmethod 
    def action(request,instance_id):
        obj_id = instance_id
        #api.nova.server_start(request, obj_id)
        return shortcuts.redirect("/project/instances/")
        