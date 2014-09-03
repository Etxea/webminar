from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView

import datetime
from models import *

class PortadaView(ListView):
    template_name="portada_webminar.html"
    model = Webminar
    #Solo listamos los viejos
    queryset = Webminar.objects.filter(fin__lt=datetime.datetime.now).order_by('-fin')
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PortadaView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        webminars_pendientes = Webminar.objects.filter(fin__gt=datetime.datetime.now).order_by('inicio')
        try:
            context['siguiente_webminar'] = webminars_pendientes[0]
            context['proximo_webminar'] = webminars_pendientes[1]
        except:
            pass
        return context

class WebminarView(DetailView):
    model = Webminar
    template_name = "webminar_ver.html"
