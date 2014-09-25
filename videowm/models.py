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
        #FIXME usar un url resolver
        return "/gestion/editar/%d/" % self.id
    def get_historico_url(self):
        return self.historico_url
    def get_view_url(self):
        #FIXME usar un url resolver
        return "/webminar/%d/ver/" % self.id
    def get_intro_url(self):
        #FIXME usar un url resolver
        return "/webminar/%d/" % self.id

class Visita(models.Model):
    fecha = models.DateTimeField(auto_now_add=True,blank=True)
    quien = models.EmailField()
    webminar = models.ForeignKey(Webminar)

class Mensaje(models.Model):
    fecha = models.DateTimeField(auto_now_add=True,blank=True)
    de = models.EmailField()
    para = models.EmailField()
    webminar = models.ForeignKey(Webminar)
    texto = models.CharField(max_length=255)
    class Meta:
        ordering = ["-fecha"]

