# -*- coding: utf-8 -*-
from django import shortcuts

    

def index(request):
    context = {}
    return shortcuts.render(request, 'index.html', context)

def gallery(request):
    context = {}
    return shortcuts.render(request, 'gallery.html', context)