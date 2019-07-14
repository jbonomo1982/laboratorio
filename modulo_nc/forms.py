from django import forms
from django.forms import ModelForm
from .models import NC , AccionInm, AnalisisCausa, AccionCorrectiva, VerificaAC, Archivo, CierreNC

class NCForm(ModelForm):

    class Meta:
        model = NC
        fields = ('titulo','descripcion','fecha_suceso','sector')
