from django.db import models
from documentos.models import Sector, Categoria_doc

# Create your models here.
class Rol(models.Model):
    #Descripcion de los puestos del laboratorio
    codigo = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    descripcion = models.TextField()


    def __str__(self):
        return '{0}'.format(self.codigo)

class Rol_usuario(models.Model):
    #Esta clase une el puesto con el usuario del sistema.
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(self.usuario,self.puesto)


class Relacion_doc_rol(models.Model):
    #Esta clase une a los documentos con los puestos de trabajo.
    documento = models.ForeignKey(Categoria_doc, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
