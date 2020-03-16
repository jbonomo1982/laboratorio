from django.urls import path
from . import views

app_name = 'p_m'
urlpatterns = [
    path('proy/', views.ProyectosListView.as_view(), name='proy'),
]