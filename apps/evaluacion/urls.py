from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('evaluacionHome/', views.evaluacionHome, name='evaluacionHome'),
    path('evaluacion_home/', login_required(views.evaluacion_home), name='evaluacion_home'),
    path('carga_masiva/', carga_masiva, name='carga_masiva'),

    path('crear_prueba/', login_required(views.crear_prueba), name='crear_prueba'),
    path('listar_pruebas/', login_required(views.listar_pruebas), name='listar_pruebas'),
    path('eliminar_prueba/<int:prueba_id>/', login_required(views.eliminar_prueba), name='eliminar_prueba' )
    # path('editar_encuesta/<int:encuesta_id>/', login_required(views.editar_encuesta), name='editar_encuesta'),

    # #RUTAS PUBLICAS
    # path('home/',   views.encuestaHome, name='encuestaHome'),
 
]