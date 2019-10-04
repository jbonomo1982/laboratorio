from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


# Create your models here.

class Sector(models.Model):

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10 ,help_text="Abreviatura del sector.")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        d =  self.codigo
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
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return '{0}'.format(self.codigo)


class Documento(models.Model):
    #Clase que guarda la version del documento, un PDF con metadatos.
    #Version 2: Un documento que se guarda por partes luego modificables
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    version = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.ForeignKey(Categoria_doc,on_delete=models.CASCADE,related_name='categoria')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    #falta restringir el tamaño del archivo.
    pertenece_a = models.ForeignKey(Categoria_doc,on_delete=models.CASCADE,related_name='pertenece_a',null=True, blank=True)
    publicado = models.BooleanField(default=False,help_text="Indica si el documento está publicado en la página.")
    editable = models.BooleanField(default=True,help_text="Indica si el documento se puede editar, si está o estuvo publicado, no se  puede")
    #si esta variable es verdadera esta version del doc está en fase de desarrollo

    def __str__(self):
        return '{0}-{1}'.format(self.categoria,self.version)

class Parte_doc(models.Model):
    #Partes del doc, con un campo que determina que posicición tienen en el mismo.
    #Puede ser texto o una imagen.
    TEXTO = "T"
    IMAGEN = "I"
    OPCIONES_TIPO =[(IMAGEN,"Imágen"),(TEXTO,"Texto")]
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    titulo = models.TextField(help_text='Título de esta parte')
    tipo = models.CharField(max_length=1, choices=OPCIONES_TIPO)
    documento= models.ForeignKey(Documento, on_delete=models.CASCADE)
    imagen = models.FileField(upload_to='archivos/',validators=[FileExtensionValidator(allowed_extensions=['jpeg','jpg','png','gif'])],blank=True,null=True)
    posicion_en_doc = models.IntegerField(help_text="posicion que tiene este campo en el documento")
    texto =models.TextField(help_text='Insertar el texto del documento')
    editable = models.BooleanField(default=True)
    #Si el doc pasa de editable a no editable, tiene que haber un proceso que cambie
    #todos las partes del documento a no editable.

    def __str__(self):
        return '{0}-{1}'.format(self.documento,self.posicion_en_doc)


class Relacion_docs(models.Model):
    #Esta clase muestra que documentos estan asociados a este.
    #Podemos controlar las relaciones entre versiones de documentos.
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documento') #El documento sobre el que se esta trabajando
    pertenece = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='pertenece', blank=True, null=True) # A que documento pertenece

    def __str__(self):
        return '{0}pertenece a {1}'.format(self.documento,self.pertenece)

class Revision_doc(models.Model):
    #Esta clase es para mostrar quien hace la Revision delos
    #Documentos, y podemos hacer un relevamiento de todas las
    #revisiones.
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    fecha_revision = models.DateField(help_text="fecha en que se hizo la Revision")
    comentario_revision = models.CharField(max_length=500)

    def __str__(self):
        return '{0} REV {1}'.format(self.documento,self.fecha_revision)
