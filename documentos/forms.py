from django import forms
from django.forms import ModelForm
from .models import Documento, Parte_doc, Relacion_docs

class DocumentoForm(ModelForm):

    class Meta:
        model = Documento
        fields = ('archivo',)

class Parte_docForm(ModelForm):
    class Meta:
        model = Parte_doc
        fields = ('titulo', 'tipo','imagen','texto',)

class Relacion_docsForm(ModelForm):
    class Meta:
        model = Relacion_docs
        fields = ('pertenece',)
