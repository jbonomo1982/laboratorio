from django.urls import path
from . import views

app_name = 'p_m'
urlpatterns = [
    path('proy/', views.ProyectosListView.as_view(), name='proy'),
    path('proy/<int:pk>/', views.ProyectosDetailView.as_view(), name='proy-detail'),
    path('tar/', views.TareasListView.as_view(), name='tar'),
    path('tar/<int:pk>/', views.TareasDetailView.as_view(), name='tar-detail'),
]