# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
import json
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    paginate_by = 10
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
        if 'password' in self.request.POST:
            print "Comprobamos el password",self.object.password,request.POST['password']
        return redirect(self.object.get_intro_url())
    def post(self, request, *args, **kwargs):
        ##Validar email
        try:
            validate_email( request.POST['email'] )
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
        except ValidationError:
            print "Email MAL le mandamos a la intro"
            return redirect(self.get_object().get_intro_url())
        
     
    def get_context_data(self, **kwargs):
        context = super(WebminarView, self).get_context_data(**kwargs)
        context['email'] = self.request.POST['email']
        return context

class WebminarDirectoView(DetailView):
    model = Webminar
    template_name = "webminar_directo.html"
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.kwargs['password']:
            print "Comprobamos el password: ",self.object.password,"versus",self.kwargs['password']
            if self.object.password==self.kwargs['password']:
                
                ##Comprobamos la hora...
                ahora = timezone.now()
                print ahora,self.object.inicio,self.object.fin
                if (self.object.inicio < ahora ) and (self.object.fin > ahora ):
                    print "Estamos en la ventana de tiempo correcta"
                    return super(WebminarDirectoView, self).get(request, *args, **kwargs)
                else:
                    print "aun no está listo"
                    return redirect("/webminar/nodisponible/")
            else:
                return redirect(self.object.get_intro_url())
                
        return redirect(self.object.get_intro_url())

class WebminarDirectoNopassView(TemplateView):
    template_name = "webminar_directo.html"

class WebminarNodisponibleView(TemplateView):
    template_name = "webminar_nodisponible.html"

@require_http_methods(["POST"])
def WebminarMandarMensaje(request, webminar_id):
    #print "hemos recibido ",request.POST
    form = MensajeForm(request.POST)
    print request.POST
    # check whether it's valid:
    if form.is_valid():
        form.save()
        data = "{ 'recibido': True }"
        #print "Mensaje guardado"
    else:
        print form.errors
        print "Mensaje NO guardado"
        data = "{ 'recibido': False. 'mensaje': '%s' }"%form.errors
    return HttpResponse(data, content_type='application/json')


class WebminarAsistentes(ListView):
    model = Visita
    template_name = "videowm/asistentes_list.html"
    def get_queryset(self):
        self.webminar = get_object_or_404(Webminar, pk=self.kwargs['webminar_id'])
        return Visita.objects.filter(webminar=self.webminar).values('quien').annotate(cuantas=Count('quien'))
        #return Visita.objects.filter(webminar=self.webminar).values('fecha','quien').annotate(dcount=Count('quien'))

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
