from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from videowm.models import *
from views import *


urlpatterns = patterns("",
    url(r"^$", WebminarGestionList.as_view(), name="webminar_gestion_lista"),
    url(r"^nuevo/$", CreateView.as_view(model=Webminar), name="webminar_nuevo"),
    url(r"^editar/(?P<pk>\d+)/$", UpdateView.as_view(model=Webminar), name="webminar_editar"),
    url(r"^borrar/(?P<pk>\d+)/$", DeleteView.as_view(model=Webminar,success_url="/gestion/"), name="webminar_borrar"),
    url(r"^realizar/(?P<pk>\d+)/$", WebminarRealizar.as_view(), name="webminar_realizar"),
    )
