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
    url(r"^(?P<pk>\d+)/$", WebminarView.as_view(), name="webminar_ver"),
    )
