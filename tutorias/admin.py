from django.contrib import admin
from .models import Materia, Tutor, Perfil, Consulta

admin.site.register(Materia)
admin.site.register(Consulta)
admin.site.register(Perfil) # Registramos Perfil para poder ver los roles en el admin

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'materia', 'get_username')
    search_fields = ('nombre', 'usuario__username', 'email')

    def get_username(self, obj):
        return obj.usuario.username
    get_username.short_description = 'Usuario de Cuenta'