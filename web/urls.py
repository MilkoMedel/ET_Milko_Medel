# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros/',views.nosotros,name='nosotros'),
    path('galeria/',views.galeria,name='galeria'),
    path('login/',views.login_view,name='login'),
    path('form/',views.form,name='form'),
    
    # CRUD URLs
    path('crud/', views.crud, name='crud'),
    path('producto_add/', views.producto_add, name='producto_add'),  # Ensure the name here is 'producto_add'
    path('producto/<int:id>/modificate/', views.producto_mod, name='producto_mod'),
    path('producto/<int:id>/delete/', views.producto_del, name='producto_del'),

    
]

