from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Create your models here.

class Proyectos(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='autor_p') #El que crea el proyecto.
    p_m = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='encargado_p',help_text="encargado del proyecto.") #El que está encargado del proyecto.
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_comienzo = models.DateField(help_text="fecha en que se comienza el proyecto", blank=True, null=True)
    fecha_final = models.DateField(help_text="fecha en que termina el proyecto", blank=True, null=True)
    publico = models.BooleanField(default= True,help_text="Indica si el proyecto puede ser visto por todos, o no.")
    nombre_proyecto = models.CharField(help_text='nombre del proyecto',max_length=50)
    descripcion = models.TextField(help_text='descripción del proyecto')
    terminado = models.BooleanField(default= False,help_text="Indica si el proyecto está terminado")

    def __str__(self):
        d = self.nombre_proyecto
        return d

class Tareas(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='autor_t') #El que crea el proyecto.
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_comienzo = models.DateField(help_text="fecha en que comienza la tarea", blank=True, null=True)
    fecha_final = models.DateField(help_text="fecha en que termina la tarea", blank=True, null=True)
    publico = models.BooleanField(default= True,help_text="Indica si el proyecto puede ser visto por todos, o no.")
    nombre_tarea = models.CharField(help_text='nombre del proyecto',max_length=50)
    descripcion = models.TextField(help_text='descripción del proyecto')
    terminado = models.BooleanField(default= False,help_text="Indica si el proyecto está terminado")
    adjunto = models.FileField(upload_to='archivos/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)

    def __str__(self):
        d = self.nombre_tarea
        return d