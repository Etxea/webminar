from django.db import models

# Create your models here.

class Webminar(models.Model):
    slug = models.CharField('ID',max_length=25,)
    descripcion = models.CharField('Descripcion',max_length=255,)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    historico_url = models.CharField(default="#",null=True,max_length=250)
    def __unicode__(self):
        return "%s"%(self.id_slug)
    def get_absolute_url(self):
        return "/gestion/editar/%d/" % self.id
    def get_historico_url(self):
        return self.historico_url
    def get_view_url(self):
        return "/webminar/%d/" % self.id

class Visita(models.Model):
    fecha = models.DateTimeField()
    quien = models.EmailField()
    webminar = models.ForeignKey(Webminar)

class Mensaje(models.Model):
    fecha = models.DateTimeField()
    de = models.EmailField()
    para = models.EmailField()
    webminar = models.ForeignKey(Webminar)
