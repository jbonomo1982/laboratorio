from django.db import models
from documentos.models import Sector, Categoria_doc

# Create your models here.
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
    nombre = models.CharField(max_length=200,help_text="Poner el nombre del instrumento si es referido en el documento, para que sea fácil encontrarlo")
    codigo = models.CharField(max_length=200,default= "Genérico", help_text="Poner el código del instrumento si es referido en el documento, para que sea fácil encontrarlo")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,blank=True,null=True)
    descripcion = models.TextField()

    def __str__(self):
        return '{0} {1}'.format(self.clase,self.codigo)

class Relacion_instr_doc(models.Model):
    #Esta clase guarda en que documento está nombrado un instrumento (puede ser)
    #uno genérico un instrumento en especifico
    documento = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
