from adminBoard.models import Appliance_type
def appliance_list(request):
    appliance_list = Appliance_type.objects.filter()
    return {"appliance_list":appliance_list}