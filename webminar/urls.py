from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy

from django.contrib import admin


urlpatterns = patterns("",
    url(r"^$", RedirectView.as_view(url=reverse_lazy('webminar_portada')), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^webminar/", include("videowm.urls")),
    url(r"^gestion/", include("gestion.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
