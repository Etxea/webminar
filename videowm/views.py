# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
import json
from django.http import HttpResponse

from django.db.models import Q
from django.db.models import Count

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
        webminars_pendientes = Webminar.objects.filter(fin__gt=datetime.datetime.now).order_by('-inicio')
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
        if 'password' in self.request.POST:
            print "Comprobamos el password",self.object.password,request.POST['password']
        return redirect(self.object.get_intro_url())
    def post(self, request, *args, **kwargs):
        ##FIXME comprobar la contraseña
        
        ##Apuntar una visita
        if 'password' in self.request.POST:
            print "Comprobamos el password",request.POST['password']
            if request.POST['password']==self.get_object().password:
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
            else:
                print "Password MAL le mandamos a la intro"
                return redirect(self.get_object().get_intro_url())
        else:
            print "No hay password le mandamos a la intro"
            return redirect(self.get_object().get_intro_url())
     
    def get_context_data(self, **kwargs):
        context = super(WebminarView, self).get_context_data(**kwargs)
        context['email'] = self.request.POST['email']
        return context
        

@require_http_methods(["POST"])
def WebminarMandarMensaje(request, webminar_id):
    #print "hemos recibido ",request.POST
    form = MensajeForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        form.save()
        data = "{ 'recibido': True }"
        #print "Mensaje guardado"
    else:
        #print form.errors
        #print "Mensaje NO guardado"
        data = "{ 'recibido': False. 'mensaje': '%s' }"%form.errors
    return HttpResponse(data, content_type='application/json')


class WebminarAsistentes(ListView):
    model = Visita
    template_name = "videowm/asistentes_list.html"
    def get_queryset(self):
        self.webminar = get_object_or_404(Webminar, pk=self.kwargs['webminar_id'])
        return Visita.objects.filter(webminar=self.webminar).values('fecha','quien').annotate(dcount=Count('quien'))

##Esto enseña todos los mensajes, solo para admin
## FIXNE hace falta estar logeado!
class WebminarLeerTodosMensajes(ListView):
    model = Mensaje
    template_name = "webminar_mensajes.html"
    def get_queryset(self):
        self.webminar = get_object_or_404(Webminar, pk=self.kwargs['webminar_id'])
        return Mensaje.objects.filter(webminar=self.webminar).order_by('fecha')

##Esto muestra solo los mensajes de o para el email y los que son para all
class WebminarLeerMensajes(ListView):
    model = Mensaje
    template_name = "webminar_mensajes.html"
    def get_queryset(self):
        #print self.kwargs
        email = self.kwargs['email']
        #print "Vamos a buscar los mensajes para",email
        self.webminar = get_object_or_404(Webminar, pk=self.kwargs['webminar_id'])
        return Mensaje.objects.filter(Q(webminar=self.webminar)&((Q(de=email) | Q(para=email) | Q(para="all@all.all")))).order_by('fecha')
