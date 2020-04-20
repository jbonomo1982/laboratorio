from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyectos , Tareas
from django.views import generic
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.
class ProyectosListView(generic.ListView):
    model = Proyectos
    paginate_by = 10 #Paginación.
    #Se hace una busqueda más detallada de Documentos, para que busque solo los publicados.
    def get_queryset(self):
        queryset = super(ProyectosListView, self).get_queryset()
        return queryset.filter(publico=True)


class ProyectosDetailView(generic.DetailView):
    model = Proyectos


class TareasListView(generic.ListView):
    model = Tareas
    paginate_by = 10 #Paginación.


class TareasDetailView(generic.DetailView):
    model = Tareas
