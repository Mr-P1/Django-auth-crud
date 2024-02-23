
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('tareas/',views.tareas,name='tareas'),
    path('logout/',views.cerrar_sesion,name='logout'),
    path('signin/',views.iniciar_sesion,name='signin'),
    path('tareas/crear/',views.crear_tareas,name='crear_tarea'),
    path('tareas/detalle/<int:id>/',views.detalle_tarea,name='detalle_tarea'),
    path('tareas/detalle/<int:id>/completado',views.completado,name='completado'),
    path('tareas/detalle/<int:id>/no_completado',views.no_completado,name='no_completado'),
    path('tareas/detalle/<int:id>/eliminar',views.eliminar_tarea,name='eliminar')
]
