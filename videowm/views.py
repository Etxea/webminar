# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
import json
from django.http import HttpResponse

import datetime
from models import *
from forms import *

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

class WebminarIntroView(DetailView):
    model = Webminar
    template_name = "webminar_intro.html"

class WebminarView(DetailView):
    model = Webminar
    template_name = "webminar_ver.html"
    #leemos el email y añadimos una visita
    ##Si es un get lo reenviamos a la intro
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object.get_intro_url())
    def post(self, request, *args, **kwargs):
        ##FIXME comprobar la contraseña
        ##Apuntar una visita
        #print self.request
        #print self.request.POST
        if 'email' in self.request.POST:
            print "Nos visita ",request.POST['email']
            visita = Visita(webminar=self.get_object(),quien=request.POST['email'])
            print "Creando visita"
            visita.save()
            print "Visita guardada"
            return super(WebminarView, self).get(request, *args, **kwargs)
        else:
            print "No hay email el mandamos a la intro"
            return redirect(self.get_object().get_intro_url())
     
    def get_context_data(self, **kwargs):
        context = super(WebminarView, self).get_context_data(**kwargs)
        context['email'] = self.request.POST['email']
        return context
        

@require_http_methods(["POST"])
def WebminarMandarMensaje(request, webminar_id):
    print "hemos recibido ",request.POST
    form = MensajeForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        form.save()
        data = "{ 'recibido': True }"
        print "Mensaje guardado"
    else:
        print form.errors
        print "Mensaje NO guardado"
        data = "{ 'recibido': False. 'mensaje': '%s' }"%form.errors
    return HttpResponse(data, content_type='application/json')
    
class WebminarLeerMensajes(ListView):
    model = Mensaje
    template_name = "webminar_mensajes.html"
