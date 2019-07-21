from django import forms
from django.forms import ModelForm
from .models import NC , AccionInm, AnalisisCausa, AccionCorrectiva, VerificaAC, Archivo, CierreNC

class NCForm(ModelForm):

    class Meta:
        model = NC
        fields = ('titulo','descripcion','fecha_suceso','sector')

class AccionInmForm(ModelForm):

    class Meta:
        model = AccionInm
        fields = ('descripcion',)

class AccionInmFormEditor(ModelForm):

    class Meta:
        model = AccionInm
        fields = ('publicado',)

class AnalisisForm(ModelForm):

    class Meta:
        model = AnalisisCausa
        fields = ('descripcion',)

class AnalisisFormEditor(ModelForm):

    class Meta:
        model = AnalisisCausa
        fields = ('publicado',)

class AccionCorrectivaForm(ModelForm):

    class Meta:
        model = AccionCorrectiva
        fields = ('descripcion','fecha_limite',)

class AccionCorrectivaFormEditor(ModelForm):

    class Meta:
        model = AccionCorrectiva
        fields = ('publicado',)

class VerificaACForm(ModelForm):

    class Meta:
        model = VerificaAC
        fields = ('encargado','fecha_verificacion', 'resultado','metodo_verificacion',)

class VerificaACFormEditor(ModelForm):

    class Meta:
        model = VerificaAC
        fields = ('publicado',)

class ArchivoForm(ModelForm):

    class Meta:
        model = Archivo
        fields = ('archivo','descripcion',)

class ArchivoFormEditor(ModelForm):

    class Meta:
        model = Archivo
        fields = ('publicado',)

class CierreNCForm(ModelForm):

    class Meta:
        model = CierreNC
        fields = ('observacion',)

class CierreNCFormEditor(ModelForm):

    class Meta:
        model = CierreNC
        fields = ('aceptado',)
