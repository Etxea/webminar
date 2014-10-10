# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required

from videowm.models import *

class WebminarGestionList(ListView):
    model=Webminar
    paginate_by = 3
    template_name="videowm/webminar_gestion_list.html"


class WebminarRealizar(DetailView):
    model=Webminar
    template_name="videowm/webminar_realizar.html"

import csv
from django.http import HttpResponse

def exportar_mensajes(request,pk):
    webminar = get_object_or_404(Webminar, pk=pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mensajes_%s.csv"'%webminar.slug
    writer = csv.writer(response,delimiter=';')
    writer.writerow(['Fecha', 'De', 'Para', 'Texto'])
    for mensaje in webminar.mensaje_set.all().order_by('-fecha'):
		print mensaje.fecha, mensaje.de, mensaje.para, mensaje.texto
		writer.writerow([mensaje.fecha, mensaje.de, mensaje.para, mensaje.texto.encode("utf-8")])
    return response

def exportar_visitas(request,pk):
    webminar = get_object_or_404(Webminar, pk=pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitas_%s.csv"'%webminar.slug
    writer = csv.writer(response,delimiter=';')
    writer.writerow(['Fecha', 'Quien'])
    for mensaje in webminar.visita_set.all().order_by('-fecha'):
        writer.writerow([mensaje.fecha, mensaje.quien])
    return response
