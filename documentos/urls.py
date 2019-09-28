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
]
