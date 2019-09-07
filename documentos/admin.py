from django.contrib import admin
from .models import Sector, Tipo_doc, Categoria_doc, Documento, Relacion, Instrumento, Relacion_instr_doc, Puesto, Rol_usuario, Relacion_doc_puesto
# Register your models here.
admin.site.register(Sector)
admin.site.register(Tipo_doc)
admin.site.register(Categoria_doc)
admin.site.register(Documento)
admin.site.register(Relacion)
admin.site.register(Instrumento)
admin.site.register(Relacion_instr_doc)
admin.site.register(Puesto)
admin.site.register(Rol_usuario)
admin.site.register(Relacion_doc_puesto)
