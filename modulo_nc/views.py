from django.shortcuts import render
from django.views import generic
from .models import NC
from .forms import NCForm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.

def prueba(request):
    return render(request, 'modulo_nc/prueba.html', {})

class NCListView(generic.ListView):
    model = NC

class NCDetailView(generic.DetailView):
    model = NC

def nc_new(request):
    tipo = "No Conformidad"
    if request.method == "POST":
        form = NCForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            c = Contribuyente(nc=NC.objects.get(pk = post.pk))
            c.save()
            return redirect('nc-detail', pk=post.pk)
    else:
        form = NCForm()
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form})
