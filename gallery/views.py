# Create your views here.
from django import shortcuts
def index(request):
    context = {"role":""}
    return shortcuts.render(request, 'gallery/index.html', context)
