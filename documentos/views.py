from django.shortcuts import render
from .models import Documento, Categoria_doc, Parte_doc
from modulo_nc.models import NC
from .forms import DocumentoForm
from django.views import generic
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.
def index(request):
    nc = NC.objects.all().count()
    doc = Documento.objects.all().count()
    return render(request, 'documentos/index.html', {'nc':nc,'doc':doc})

class DocumentoListView(generic.ListView):
    model = Documento
    paginate_by = 10 #Paginación.
    #Se hace una busqueda más detallada de Documentos, para que busque solo los publicados.
    def get_queryset(self):
        queryset = super(DocumentoListView, self).get_queryset()
        return queryset.filter(publicado=True)

class DocumentoDetailView(generic.DetailView):
    model = Documento

def doc_new(request, pk):
    doc = Documento.objects.get(pk=pk)
    #Se ponen los datos del documento del cual se quiere crear una
    #nueva versión.
    if request.method == "POST":
        form = DocumentoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.categoria = doc.categoria

            post.save()
            return redirect('doc-detail', pk=post.pk)
    else:
        form = DocumentoForm()
    return render(request, 'documentos/nuevo_doc.html', {'form': form})


class Categoria_docListView(generic.ListView):
    model = Categoria_doc
    paginate_by = 10 #Paginación.


class Categoria_docDetailView(generic.DetailView):
    model = Categoria_doc

def cat_doc_detalle(request):
    cat_doc_requerido = request.GET['CD']
    cat_doc_buscada = Categoria_doc.objects.get(pk=cat_doc_requerido)
    #Buscamos todas las versiones de este documento que hay disponibles.
    docs = Documento.objects.filter(categoria = cat_doc_buscada)

    return render(request, 'documentos/cat_doc_detalle.html', {'cat':cat_doc_buscada, 'docs':docs})

def Docu_detallado(request,pk):
    docu_buscado = Documento.objects.get(pk=pk)
    partes = Parte_doc.objects.filter(documento=docu_buscado).order_by('posicion_en_doc')

    return render(request, 'documentos/documento_detail.html',{'documento':docu_buscado,'partes':partes})
