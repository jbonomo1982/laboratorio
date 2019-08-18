from django.urls import path
from . import views

app_name = 'nc'
urlpatterns = [
    path('prueba', views.prueba, name='prueba'),
    path('nc/', views.NCListView.as_view(), name='nc'),
    path('nc/<int:pk>/',views.NCDetailView.as_view(),name='nc-detail'),
    path('nuevanc', views.nc_new, name='nuevanc'),
    path('nc_informe/<int:pk>/',views.nc_info,name='nc-info'),
    path('AccionInm/<int:pk>/',views.AccionInmDetailView.as_view(),name='AccionInm-detail'),
    path('accionInm_por_NC', views.accionInm_por_NC, name='accionInm_por_NC'),
    path('AccionInm_edit/<int:pk>/',views.AccionInm_edit,name='AccionInm-edit'),
    path('AccionInm_publicar/<int:pk>/',views.AccionInm_publicar,name='AccionInm-publicar'),
    path('nuevaAccionInm/<int:pk>/', views.AccionInm_new, name='nuevaAccionInm'),
    path('nuevaAnalisiscausa/<int:pk>/', views.analisiscausa_new, name='nuevaAnalisis'),
    path('AnalisisCausa/<int:pk>/',views.AnalisisCausaDetailView.as_view(),name='AnalisisCausa-detail'),
    path('AnalisisCausa_por_NC', views.analisiscausa_por_NC, name='analisiscausa_por_NC'),
    path('Analisis_publicar/<int:pk>/',views.AnalisisCausa_publicar,name='Analisis-publicar'),
    path('Analisis_edit/<int:pk>/',views.AnalisisCausa_edit,name='Analisis-edit'),
    path('nuevaAccionCorrectiva/<int:pk>/', views.accioncorrectiva_new, name='nuevaAccionCorrectiva'),
    path('AccionCorrectiva/<int:pk>/',views.AccionCorrectivaDetailView.as_view(),name='AccionCorrectiva-detail'),
    path('AccionCorrectiva_por_NC', views.accioncorrectiva_por_NC, name='accioncorrectiva_por_NC'),
    path('AccionCorrectiva_publicar/<int:pk>/',views.AccionCorrectiva_publicar,name='AccionCorrectiva-publicar'),
    path('AccionCorrectiva_edit/<int:pk>/',views.AccionCorrectiva_edit,name='AccionCorrectiva-edit'),
    path('nuevaVerificacion/<int:pk>/', views.verificacionAC_new, name='nuevaVerificacion'),
    path('Verificacion/<int:pk>/',views.VerificaACDetailView.as_view(),name='VerificaAC-detail'),
    path('Verificacion_por_AC', views.verificacionAC_por_AC, name='verificacion_por_AC'),
    path('Verificacion_publicar/<int:pk>/',views.verificacion_publicar,name='Verificacion-publicar'),
    path('Archivo/<int:pk>/',views.ArchivoDetailView.as_view(),name='Archivo-detail'),
    path('nuevaArchivo/<int:pk>/', views.archivo_new, name='nuevaArchivo'),
    path('Archivo_por_NC', views.archivo_por_NC, name='archivo_por_NC'),
    path('Archivo_publicar/<int:pk>/',views.Archivo_publicar,name='Archivo-publicar'),
    path('nuevaCierreNC/<int:pk>/', views.cierreNC_new, name='nuevaCierreNC'),
    path('cerrarNC/<int:pk>/',views.CierreNCDetailView.as_view(),name='CierreNC-detail'),
    path('cierreNC_por_NC', views.cierreNC_por_NC, name='CierreNC_por_NC'),
    path('cierreNC_publicar/<int:pk>/',views.cierreNC_publicar,name='cierreNC-publicar'),


]
