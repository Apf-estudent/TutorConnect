from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('materias/', views.materias, name='materias'),
    path('respuestas/', views.respuestas, name='respuestas'),
    path('consultas/', views.consultas, name='consultas'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('tutor/', views.registrar_tutor, name='tutor'), 
    path('panel-control/usuarios/', views.lista_usuarios, name='lista_usuarios'), # 👈 Esta es la buena
    path('materias/<int:materia_id>/tutores/', views.ver_tutores_materia, name='ver_tutores_materia'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]