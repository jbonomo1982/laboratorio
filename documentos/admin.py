from django.contrib import admin
from .models import Sector, Tipo_doc, Categoria_doc, Documento, Relacion
# Register your models here.
admin.site.register(Sector)
admin.site.register(Tipo_doc)
admin.site.register(Categoria_doc)
admin.site.register(Documento)
admin.site.register(Relacion)
