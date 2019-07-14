from django.urls import path
from . import views

app_name = 'nc'
urlpatterns = [
    path('prueba', views.prueba, name='prueba'),
    path('nc/', views.NCListView.as_view(), name='nc'),
    path('nc/<int:pk>/',views.NCDetailView.as_view(),name='nc-detail'),
    path('nuevanc', views.nc_new, name='nuevanc'),

]
