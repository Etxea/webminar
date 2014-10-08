from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from videowm.models import *
from videowm.forms import *
from views import *


urlpatterns = patterns("",
    url(r"^$", login_required(WebminarGestionList.as_view()), name="webminar_gestion_lista"),
    url(r"^nuevo/$", login_required(CreateView.as_view(model=Webminar,form_class=WebminarForm)), name="webminar_nuevo"),
    url(r"^editar/(?P<pk>\d+)/$", login_required(UpdateView.as_view(model=Webminar,form_class=WebminarForm)), name="webminar_editar"),
    url(r"^borrar/(?P<pk>\d+)/$", login_required(DeleteView.as_view(model=Webminar,success_url="/gestion/")), name="webminar_borrar"),
    url(r"^realizar/(?P<pk>\d+)/$", login_required(WebminarRealizar.as_view()), name="webminar_realizar"),
    url(r"^exportar/(?P<pk>\d+)/mensajes/$", exportar_mensajes, name="webminar_exportar_mensajes"),
    url(r"^exportar/(?P<pk>\d+)/visitas/$", exportar_visitas, name="webminar_exportar_visitas"),
    )
