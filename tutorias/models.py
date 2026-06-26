from django.db import models
from django.contrib.auth.models import User

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Tutor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_tutor')
    nombre = models.CharField(max_length=100)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='tutores_principal')
    materia_2 = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True, related_name='tutores_secundario')
    descripcion = models.TextField()
    contacto = models.TextField()
    email = models.EmailField()

class Tutoria(models.Model):
    alumno = models.CharField(max_length=100)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.alumno} - {self.tutor.nombre}"

class Perfil(models.Model):
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('tutor', 'Tutor'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
class Consulta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('respondida', 'Respondida'),
    ]
    usuario_estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_consultas')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    pregunta = models.TextField()
    respuesta_tutor = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)