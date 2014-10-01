from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView


from videowm.models import *
from videowm.views import *

urlpatterns = patterns("",
    url(r"^$", PortadaView.as_view(), name="webminar_portada"),
    url(r"^(?P<pk>\d+)/$", WebminarIntroView.as_view(), name="webminar_intro"),
    url(r"^(?P<pk>\d+)/ver/$", WebminarView.as_view(), name="webminar_ver"),
    url(r"^(?P<webminar_id>\d+)/mensaje/enviar/$", WebminarMandarMensaje, name="webminar_mandar_mensaje"),
    url(r"^(?P<webminar_id>\d+)/mensaje/leer/$", WebminarLeerTodosMensajes.as_view(), name="webminar_leer_todos_mensajes"),
    url(r"^(?P<webminar_id>\d+)/mensaje/leer/(?P<email>.+)/$", WebminarLeerMensajes.as_view(), name="webminar_leer_mensajes"),
    )
