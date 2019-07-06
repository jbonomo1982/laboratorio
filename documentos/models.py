from django.db import models
from django.utils import timezone


# Create your models here.

class Sector(models.Model):

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10 ,help_text="Abreviatura del sector.")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        d = "Sector " + self.codigo
        return d

class Tipo_doc(models.Model):
    #Es el tipo de documento, si es un Proceso Operativo, un Anexo, etc...
    codigo = models.CharField(max_length=10 ,help_text="Abreviatura del tipo de documento.")
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        d = self.codigo
        return d


class Categoria_doc(models.Model):
    #Es el contenedor del documento en si, acá se definen los documentos.
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo_doc, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=200)
    sector = models.ForeignKey(Sector, default=None, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return '{0} {1}'.format(self.tipo,self.codigo)


class Documento(models.Model):
    #Clase que guarda la version del documento, un PDF con metadatos.
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria_doc,on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/') #Restringir a PDF
    publicado = models.BooleanField(default=False,help_text="Indica si el documento está publicado en la página.")

    def __str__(self):
        return '{0} {1}'.format(self.categoria,self.version)


class Relacion(models.Model):
    #Esta clase muestra la Relacion entre dos categorias de documentos
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documento')
    pertenece = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='pertenece')

    def __str__(self):
        return self.documento
