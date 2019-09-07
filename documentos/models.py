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
        return '{0} {1}'.format(self.tipo,self.codigo)


class Documento(models.Model):
    #Clase que guarda la version del documento, un PDF con metadatos.
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria_doc,on_delete=models.CASCADE,related_name='categoria')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    #falta restringir el tamaño del archivo.
    publicado = models.BooleanField(default=False,help_text="Indica si el documento está publicado en la página.")

    def __str__(self):
        return '{0} {1}'.format(self.categoria,self.version)


class Relacion(models.Model):
    #Esta clase muestra la Relacion entre dos categorias de documentos
    documento = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE, related_name='documento')
    pertenece = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE, related_name='pertenece')

class calibrador_modelo(models.Model):
    ROCHE = "Roche"
    ABBOT = "Abbot"
    RANDOX = "Ran"
    TSH_801 = "4738551190"
    FT3_801 = "4738551190"
    #las variables de opciones no tienen que tener más 5 caracteres
    OPCIONES_FABRICANTE =[(ROCHE,'Roche'),(ABBOT,'Abbot'),(RANDOX,'Randox')]
    OPCIONES_CALIBRADOR =[(TSH_801,'Calibrador TSH, para 801, Roche'),(FT3_801,'Calibrador FT3, para 801, Roche')]
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    marca = models.CharField(max_length=5, choices=OPCIONES_FABRICANTE)
    nombre = models.CharField(max_length=10, choices=OPCIONES_CALIBRADOR)
    descripcion = models.TextField()
    duracion= None #Es la duracion de las alicuotas.

    def __str__(self):
        return '{0} {1}'.format(self.descripcion,self.marca)

class calibrador(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    calibrador =models.ForeignKey(calibrador_modelo, on_delete=models.CASCADE)
    lote = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{0} {1}'.format(self.calibrador,self.lote)


class Registro_prep(models.Model):
    #Esta clase es el registro de la preparación  de calibradores,
    #puede ser que se comparta
    #entre sectores pero en principio y preparaciones, es solo para Endocrino.
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    codigo = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE)
    material = models.ForeignKey(calibrador, on_delete=models.CASCADE)
    #pipeta=None
    #contenedor=None
    #ambiente=None
    #agua_dest_tipo = None
    #agua_dest_lote = None
    #agua_dest_venc = None
    #fecha_preparacion=None
    #cantidad_alicuotas = None

    def __str__(self):
        return '{0}'.format(self.material)

class Instrumento(models.Model):
    #En esta clase se guardan los instrumentos analiticos, de medición y
    #otros que se pueden asociar a un documento. Para así hacer más facil
    #la busqueda del alcance de un documento.
    MEDICION = "M"
    ANALITICO = "A"
    OTRO = "O"
    OPCIONES_CLASE =[(MEDICION,'Medición'),(ANALITICO,'Analítico'),(OTRO,'Otro')]
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    clase = models.CharField(max_length=1, choices=OPCIONES_CLASE)
    codigo = models.CharField(max_length=200,default= "Genérico", help_text="Poner el código de el instrumento si es referido en el documento, para que sea fácil encontrarlo")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,blank=True,null=True)
    descripcion = models.TextField()

    def __str__(self):
        return '{0} {1}'.format(self.clase,self.pk)

class Relacion_instr_doc(models.Model):
    #Esta clase guarda en que documento está nombrado un instrumento (puede ser)
    #uno genérico un instrumento en especifico
    documento = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)

class Puesto(models.Model):
    #Descripcion de los puestos del laboratorio
    codigo = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    descripcion = models.TextField()


    def __str__(self):
        return '{0}'.format(self.codigo)

class Rol_usuario(models.Model):
    #Esta clase une el puesto con el usuario del sistema.
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(self.usuario,self.puesto)


class Relacion_doc_puesto(models.Model):
    #Esta clase une a los documentos con los puestos de trabajo.
    documento = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
