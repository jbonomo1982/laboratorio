from django.urls import path
from . import views

app_name = 'documentos'
urlpatterns = [
    path('', views.index, name='index'),
    path('doc/', views.DocumentoListView.as_view(), name='doc'),
    path('doc/<int:pk>/',views.DocumentoDetailView.as_view(),name='doc-detail'),
    path('nuevo_doc/<int:pk>/', views.doc_new, name='nuevo_doc'),
]
