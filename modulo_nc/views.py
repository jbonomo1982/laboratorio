from django.shortcuts import render
from django.views import generic
from .models import NC, AccionInm, Contribuyente, AnalisisCausa, AccionCorrectiva, VerificaAC, Archivo, CierreNC
from .forms import NCForm,AccionInmForm, AccionInmFormEditor, AnalisisForm, AnalisisFormEditor, AccionCorrectivaForm,AccionCorrectivaFormEditor, VerificaACForm, VerificaACFormEditor,ArchivoForm, ArchivoFormEditor, CierreNCForm, CierreNCFormEditor
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
            return redirect('nc:nc-detail', pk=post.pk)
    else:
        form = NCForm()
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form})


#Acción Inmediata:

class AccionInmDetailView(generic.DetailView):
    model = AccionInm


def AccionInm_new(request,pk):
    tipo = "Acción Inmediata"
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = AccionInmForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            post.nc = nc
            post.save()
            return redirect('nc:AccionInm-detail', pk=post.pk)
    else:

        form = AccionInmForm()
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form,'nc':nc})

def AccionInm_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    tipo = "Acción Inmediata"
    post = get_object_or_404(AccionInm, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = AccionInmForm(request.POST)

        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            b.created_date = timezone.now()
            b.save()
            return redirect('nc:AccionInm-detail', pk=b.pk)


    else:
        form = AccionInmForm(initial={'descripcion':post.descripcion})
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form})

def AccionInm_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    tipo = "Acción Inmediata"
    post = get_object_or_404(AccionInm, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":

        if grupo:
            formE = AccionInmFormEditor(request.POST,instance=post)
            if formE.is_valid():

                post2 = formE.save(commit=False)


                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAI = AccionInm.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAI.update(publicado=False)

                return redirect('nc:AccionInm-detail', pk=post2.pk)

    else:
        form = AccionInmForm(instance=post)
        formE = AccionInmFormEditor(instance=post)
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form,'formE':formE})



def accionInm_por_NC(request):
    #detalla las acc. inm por la NC
    tipo = "Acción Inmediata"
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    acc = AccionInm.objects.filter(nc=nc_buscada)
    return render(request, 'modulo_nc/x_nc.html', {'tipo':tipo,'ai':acc,'nc': nc_requerida})


#Analisis Causa:
class AnalisisCausaDetailView(generic.DetailView):
    model = AnalisisCausa


def analisiscausa_new(request,pk):
    tipo= "Análisis de Causa"
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = AnalisisForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            post.nc = nc
            post.save()
            return redirect('nc:AnalisisCausa-detail', pk=post.pk)
    else:

        form = AnalisisForm()
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form,'nc':nc})



def analisiscausa_por_NC(request):
    #detalla los analisis de causa por  NC
    tipo = "Análisis de Causa"
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    ac = AnalisisCausa.objects.filter(nc=nc_buscada)
    return render(request, 'modulo_nc/x_nc.html', {'tipo':tipo,'ac':ac,'nc': nc_requerida})


def AnalisisCausa_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    tipo = "Análisis de Causa"
    post = get_object_or_404(AnalisisCausa, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":

        if grupo:
            formE = AnalisisFormEditor(request.POST,instance=post)
            if formE.is_valid():

                post2 = formE.save(commit=False)


                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = AnalisisCausa.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(publicado=False)

                return redirect('nc:AnalisisCausa-detail', pk=post2.pk)

    else:
        form = AnalisisForm(instance=post)
        formE = AnalisisFormEditor(instance=post)
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form,'formE':formE})

def AnalisisCausa_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    tipo = "Análisis de Causa"
    post = get_object_or_404(AnalisisCausa, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = AnalisisForm(request.POST)

        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()


            b.save()
            return redirect('nc:AnalisisCausa-detail', pk=b.pk)


    else:
        form = AnalisisForm(initial={'descripcion':post.descripcion})
    return render(request, 'modulo_nc/nuevo.html', {'tipo': tipo,'form': form})

#Acción Correctiva

class AccionCorrectivaDetailView(generic.DetailView):
    model = AccionCorrectiva


def accioncorrectiva_new(request,pk):
    tipo = "Acción Correctiva"
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = AccionCorrectivaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            post.nc = nc
            post.save()
            return redirect('nc:AccionCorrectiva-detail', pk=post.pk)
    else:

        form = AccionCorrectivaForm()
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form,'nc':nc})



def accioncorrectiva_por_NC(request):
    #detalla la acc corr por  NC
    tipo = "Accion Correctiva"
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    ac = AccionCorrectiva.objects.filter(nc=nc_buscada)
    return render(request, 'modulo_nc/x_nc.html', {'tipo':tipo,'aco':ac,'nc': nc_requerida})


def AccionCorrectiva_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    tipo = "Acción Correctiva"
    post = get_object_or_404(AccionCorrectiva, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":

        if grupo:
            formE = AccionCorrectivaFormEditor(request.POST,instance=post)
            if formE.is_valid():

                post2 = formE.save(commit=False)


                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = AccionCorrectiva.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(publicado=False)

                return redirect('nc:AccionCorrectiva-detail', pk=post2.pk)

    else:
        form = AccionCorrectivaForm(instance=post)
        formE = AccionCorrectivaFormEditor(instance=post)
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form,'formE':formE})

def AccionCorrectiva_edit(request, pk):
    #Editar en realidad tiene que ser crear una nueva instancia sobre otra anterior
    tipo = "Acción Correctiva"
    post = get_object_or_404(AccionCorrectiva, pk=pk)
    nc = post.nc
    if request.method == "POST":
        form = AccionCorrectivaForm(request.POST)

        if form.is_valid():
            b= form.save(commit=False)
            b.autor = request.user
            b.nc = nc

            if nc.autor != request.user:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()


            b.save()
            return redirect('nc:AccionCorrectiva-detail', pk=b.pk)


    else:
        form = AccionCorrectivaForm(initial={'descripcion':post.descripcion})
    return render(request, 'modulo_nc/nuevo.html', {'tipo':tipo,'form': form})

#Verificación AC

class VerificaACDetailView(generic.DetailView):
    model = VerificaAC


def verificacionAC_new(request,pk):
    tipo = "verificación de Acción Correctiva"
    #Se hace solo verificacion si hay una AC publicada y se hacen verificaciones solo sobre la misma.
    ac = get_object_or_404(AccionCorrectiva, pk=pk,publicado=True)#filtra por publicado
    nc = ac.nc
    print(nc.pk)
    if request.method == "POST":
        form = VerificaACForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.nc = nc
            post.ac = ac
            post.autor = request.user
            post.save()
            return redirect('nc:VerificaAC-detail', pk=post.pk)
        else:
            print("no es válido")
    else:

        form = VerificaACForm()

    return render(request, 'modulo_nc/nuevo.html', {'form': form,'ac':ac, 'tipo':tipo})



def verificacionAC_por_AC(request):
    #detalla la verificación de AC por  AC
    pk_ac = request.GET['AC']
    ac = AccionCorrectiva.objects.get(pk=pk_ac)
    vac = VerificaAC.objects.filter(ac=ac)

    return render(request, 'modulo_nc/verificacionAC_x_ac.html', {'vac':vac,'ac': ac})


def verificacion_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    tipo="verificación de Acción Correctiva"
    post = get_object_or_404(VerificaAC, pk=pk)
    usuario_req = request.user.username

    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":

        if grupo:
            formE = VerificaACFormEditor(request.POST,instance=post)
            if formE.is_valid():

                post2 = formE.save(commit=False)


                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    ac = post2.ac
                    print(ac)
                    otrasVAC = VerificaAC.objects.filter(ac = ac).exclude(pk=post2.pk)
                    otrasVAC.update(publicado=False)

                return redirect('nc:VerificaAC-detail', pk=post2.pk)

    else:
        form = VerificaACForm(instance=post)
        formE = VerificaACFormEditor(instance=post)
    return render(request, 'modulo_nc/nuevo.html', {'form': form,'formE':formE,'tipo':tipo})


#Archivo

class ArchivoDetailView(generic.DetailView):
    model = Archivo


def archivo_new(request,pk):
    tipo = "Archivo"
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            post.nc = nc
            post.save()
            return redirect('nc:Archivo-detail', pk=post.pk)
    else:

        form = ArchivoForm()
    return render(request, 'modulo_nc/nuevo.html', {'form': form,'nc':nc, 'tipo':tipo})



def archivo_por_NC(request):
    #detalla la archivos por  NC
    tipo = "Archivo"
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    ar = Archivo.objects.filter(nc=nc_buscada)
    return render(request, 'modulo_nc/x_nc.html', {'ar':ar,'nc': nc_requerida, 'tipo':tipo})


def Archivo_publicar(request, pk):
    #Solo los usuarios editores pueden publicar.
    tipo = "Archivo"
    post = get_object_or_404(Archivo, pk=pk)
    usuario_req = request.user.username
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":

        if grupo:
            formE = ArchivoFormEditor(request.POST,instance=post)
            if formE.is_valid():

                post2 = formE.save(commit=False)


                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de AI de la misma NC a no publicado.
                if post2.publicado == True:
                    print("publicado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = Archivo.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(publicado=False)

                return redirect('nc:Archivo-detail', pk=post2.pk)

    else:
        form = ArchivoForm(instance=post)
        formE = ArchivoFormEditor(instance=post)
    return render(request, 'modulo_nc/nuevo.html', {'form': form,'formE':formE,'tipo':tipo})

#Informe de NC
def nc_info(request, pk):
    #esta view es para ver lo publicado en de una NC
    nc = get_object_or_404(NC, pk=pk)

    #buscar la accion inmediata publicada
    ai_de_nc = AccionInm.objects.filter(nc=nc).exclude(publicado=False)
    ai = None
    for a in ai_de_nc:
        if a.publicado == True:
            ai = a
        else:
            ai = None

    #buscar el analisis de causa publicado
    ac_de_nc = AnalisisCausa.objects.filter(nc=nc).exclude(publicado=False)
    ac =None
    for a in ac_de_nc:
        if a.publicado == True:
            ac = a
        else:
            ac = None
    #buscar la accion correctiva publicada
    aco_de_nc = AccionCorrectiva.objects.filter(nc=nc).exclude(publicado=False)
    aco = None
    for a in aco_de_nc:
        if a.publicado == True:
            aco = a
        else:
            aco = None
    #buscar la verificacion  de la AC publicada
    vac_de_ac = VerificaAC.objects.filter(ac = aco).exclude(publicado=False)
    vac = None
    for v in vac_de_ac:
        if v.publicado == True:
            vac = v
        else:
            vac = None

    #buscar el cierre de la NC
    cie_NC = CierreNC.objects.filter(nc=nc).exclude(aceptado=False)
    cNC = None
    for c in cie_NC:
        if c.aceptado == True:
            cNC = c

    return render(request, 'modulo_nc/nc_info.html', {'nc':nc,'ai':ai,'ac':ac,'aco':aco,'vac':vac, 'cNC':cNC })



# Cierre de NC

class CierreNCDetailView(generic.DetailView):
    model = CierreNC

def cierreNC_new(request,pk):
    tipo = "Cierre de NC"
    nc = NC.objects.get(pk=pk)
    if request.method == "POST":
        form = CierreNCForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            if nc.autor != post.autor:
                if Contribuyente.objects.get(nc=nc):
                    a = Contribuyente.objects.get(nc=nc)
                    a.contribuyente.add(request.user)
                    a.save()

            post.nc = nc
            post.save()
            return redirect('CierreNC-detail', pk=post.pk)
    else:

        form = CierreNCForm()
    return render(request, 'modulo_nc/nuevo.html', {'form': form,'nc':nc,'tipo':tipo})



def cierreNC_por_NC(request):
    #detalla la acc corr por  NC
    tipo = "Cierre de NC"
    nc_requerida = request.GET['NC']
    nc_buscada = NC.objects.get(pk=nc_requerida)
    cNC = CierreNC.objects.filter(nc=nc_buscada)
    return render(request, 'modulo_nc/x_nc.html', {'cNC':cNC,'nc': nc_requerida,'tipo':tipo})


def cierreNC_publicar(request, pk):
    tipo = "Cierre de NC"
    #Solo los usuarios editores pueden publicar.
    post = get_object_or_404(CierreNC, pk=pk)
    usuario_req = request.user.username
    usuario_Ai = post.autor
    grupo = request.user.groups.filter(name='Editor_Responsable').exists()
    if not grupo:
        return HttpResponse("Tiene que tener un usuario con perfil de editor. " + str(usuario_req))
    if request.method == "POST":

        if grupo:
            formE = CierreNCFormEditor(request.POST,instance=post)
            if formE.is_valid():

                post2 = formE.save(commit=False)


                post2.save()
                #Si se cambia el estado a publicado, tiene que cambiar todos los
                #otros ingresos de Cierre de NC de la misma NC a no publicado.
                if post2.aceptado == True:
                    print("aceptado")
                    nc = post2.nc
                    print(nc)
                    otrasAC = CierreNC.objects.filter(nc = nc).exclude(pk=post2.pk)
                    otrasAC.update(aceptado=False)
                    #Cambia el estado de la NC
                    cierre = NC.objects.filter(pk = nc.pk).update(cerrada = True)


                return redirect('CierreNC-detail', pk=post2.pk)

    else:
        form = CierreNCForm(instance=post)
        formE = CierreNCFormEditor(instance=post)
    return render(request, 'modulo_nc/nuevo.html', {'form': form,'formE':formE,'tipo':tipo})
