from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView

from videowm.models import *

class WebminarGestionList(ListView):
    model=Webminar
    template_name="videowm/webminar_gestion_list.html"


class WebminarRealizar(DetailView):
    model=Webminar
    template_name="videowm/webminar_realizar.html"
