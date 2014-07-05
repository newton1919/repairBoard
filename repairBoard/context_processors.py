from adminBoard.models import Appliance_type, Company
def appliance_list(request):
    appliance_list = Appliance_type.objects.filter()
    return {"appliance_list":appliance_list}

def company_info(request):
    company = Company.objects.filter()[0]
    return {"company_info": company}