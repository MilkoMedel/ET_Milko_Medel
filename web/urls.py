# from django.conf.urls import url
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # pagina
    path('', views.index, name='index'),
    path('nosotros/',views.nosotros,name='nosotros'),
    path('galeria/',views.galeria,name='galeria'),
    path('login/',views.login_view,name='login'),
    path('form/',views.form,name='form'),
    path('perfil/', views.perfil, name='perfil'),
    path('mostrar_perfil', views.mostrar_perfil, name='mostrar_perfil'),
    
    # CRUD URLs

    path('crud/', views.crud, name='crud'),
    path('producto', views.producto, name='producto'),
    path('producto_add/', views.producto_add, name='producto_add'),  # Ensure the name here is 'producto_add'
    path('producto/<int:id>/modificate/', views.producto_mod, name='producto_mod'),
    path('producto/<int:id>/delete/', views.producto_del, name='producto_del'),

    # carrito URLs
    path('carrito/', views.mostrar_carrito, name='mostrar_carrito'),
    # Otras rutas del carrito
    path('carrito_prod/add/<id>', views.agregar_producto, name="carrito_prod_add"),
    path('carrito_prod/substract/<id>', views.restar_producto, name="carrito_prod_substract"),
    path('carrito_prod/delete/<id>', views.eliminar_producto, name="carrito_prod_delete"),
    path('carrito_prod/clear', views.limpiar_carrito, name="carrito_prod_clear"),
    path('carrito_prod/open', views.carrito_prod_open, name="carrito_prod_open"),
    path('carrito_prod/close', views.carrito_prod_close, name="carrito_prod_close"),
    path('create_order', views.create_order, name='create_order'),
    
    # restablecer contrasena urls

    path('accounts/password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
        name='password_reset'), 
    path('accounts/password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
        name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
        name='password_reset_confirm'), 
    path('accounts/reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'), 
    path('accounts/', include('django.contrib.auth.urls')), 

]

