from django.urls import path
from . import views

app_name = 'documentos'
urlpatterns = [
    path('', views.index, name='index'),
    path('doc/', views.DocumentoListView.as_view(), name='doc'),
    path('doc/<int:pk>/',views.Docu_detallado,name='doc-detalle'),
    path('nuevo_doc/<int:pk>/', views.doc_new, name='nuevo_doc'),
    path('cat_doc/<int:pk>/',views.Categoria_docDetailView.as_view(),name='cat_doc-detail'),
    path('cat', views.cat_doc_detalle, name='cat_doc_detalle'),
    path('Parte_doc_edit/<int:pk>/',views.editar_parte,name='editar_parte'),
    path('Docu_edit/<int:pk>/',views.Docu_editar,name='editar_docu'),
    path('pdf/<int:pk>/',views.generar_pdf,name='pdf'),
    path('Docu_publi/<int:pk>/',views.publicar_docu,name='publicar_docu'),
]
