from django.shortcuts import render
from .models import Documento
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
