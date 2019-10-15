from django.shortcuts import render, get_object_or_404, redirect
from .models import Documento, Categoria_doc, Parte_doc, Revision_doc, Relacion_docs
from modulo_nc.models import NC
from .forms import DocumentoForm, Parte_docForm
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
    #Agregar la relacion de documentos
    relacion = Relacion_docs.objects.filter(documento=docu_buscado)
    #Agregar revision de doc.
    revisiones = Revision_doc.objects.filter(documento= docu_buscado )

    return render(request, 'documentos/documento_detail.html',{'documento':docu_buscado,'partes':partes, 'revisiones':revisiones,'relacion':relacion})

def editar_parte(request, pk):
    parte = get_object_or_404(Parte_doc, pk=pk)
    #Agregar que solo puede editar partes Editor_Responsable y del sector
    if request.method == "POST":
        form = Parte_docForm(request.POST)

        if form.is_valid():
            b= form.save(commit=False)
            parte.titulo = b.titulo
            parte.texto = b.texto
            parte.save()
            return redirect('documentos:editar_docu', pk=parte.documento.pk)
    else:
        form = Parte_docForm(initial={'texto':parte.texto,'titulo':parte.titulo, 'tipo':parte.tipo})
    return render(request, 'documentos/editar_parte.html', {'form': form})

def Docu_editar(request, pk):
    #busca el documentos que se esta buscando
    docu = get_object_or_404(Documento, pk=pk)
    #Del documento hay que buscar si hay un editable del usuario #
    #que lo esta solicitando, si no, se crea un editable en base al publicado
    d = Documento.objects.filter(categoria=docu.categoria)
    print(Documento.objects.filter(categoria=docu.categoria).count)
    if Documento.objects.filter(categoria=docu.categoria, autor=request.user, editable=True).exists():
        #Busca exactamente el doc que estamos buscando:
        p = Documento.objects.filter(categoria=docu.categoria, autor=request.user, editable=True)
        for i in p:
            partes = Parte_doc.objects.filter(documento= i).order_by('posicion_en_doc')
            return render(request, 'documentos/docu_editar.html', {'documento':i, 'partes':partes})
    else:
        print("Se eligió el publicado")
        nuevo = docu
        nuevo.pk = None
        nuevo.save()
        nuevo.autor = request.user
        nuevo.version = "Editable"
        nuevo.fecha_creacion = timezone.now()
        nuevo.fecha_publicacion = None
        nuevo.fecha_vencimiento = None
        nuevo.publicado = False
        nuevo.editable = True
        nuevo.save()
        #Agregar la relación de documentos para que cree la instancia para
        #El nuevo documento.
        partes = Parte_doc.objects.filter(documento= Documento.objects.get(pk=pk))
        print(partes)
        for p in partes:
            print("una parte")
            nueva_p = p
            nueva_p.pk = None
            nueva_p.save()
            nueva_p.autor=request.user
            nueva_p.documento = nuevo
            nueva_p.save()

        partes_nuevo = Parte_doc.objects.filter(documento=nuevo).order_by('posicion_en_doc')

        return render(request, 'documentos/docu_editar.html', {'documento':nuevo, 'partes':partes_nuevo})
