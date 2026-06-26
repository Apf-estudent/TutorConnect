from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Tutor, Materia, Perfil, Consulta

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'tutorias/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('inicio')

def inicio(request):
    return render(request, 'tutorias/index.html')

def materias(request):
    materias_lista = Materia.objects.all()
    return render(request, 'tutorias/materias.html', {'materias_lista': materias_lista})

def ver_tutores_materia(request, materia_id):
    materia_objeto = get_object_or_404(Materia, id=materia_id)
    tutores = Tutor.objects.filter(materia=materia_objeto)
    return render(request, 'tutorias/tutores_materia.html', {
        'materia': materia_objeto,
        'tutores': tutores
    })

def respuestas(request):
    return render(request, 'tutorias/respuestas.html')

@login_required
def consultas(request):
    if request.method == 'POST':
        # Aquí procesarías el guardado de una nueva consulta...
        pass

    # 🔥 EL FILTRO CLAVE: Trae solo las consultas del usuario actual
    mis_preguntas = Consulta.objects.filter(usuario_estudiante=request.user).order_by('-fecha_creacion')
    
    tutores = Tutor.objects.all()
    
    return render(request, 'tutorias/consultas.html', {
        'consultas': mis_preguntas,
        'tutores': tutores
    })

@login_required
def registrar_tutor(request):
    tutor_existente = Tutor.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        materia_id = request.POST.get('materia_id')
        materia_id_2 = request.POST.get('materia_id_2')
        descripcion = request.POST.get('descripcion')
        email = request.POST.get('email') # Este es el dato que viene del formulario HTML

        materia_objeto = get_object_or_404(Materia, id=materia_id)
        
        materia_objeto_2 = None
        if materia_id_2:
            materia_objeto_2 = Materia.objects.filter(id=materia_id_2).first()
        
        Tutor.objects.update_or_create(
            usuario=request.user,
            defaults={            
                'nombre': nombre,
                'materia': materia_objeto,
                'materia_2': materia_objeto_2,
                'descripcion': descripcion,
                'contacto': email 
            })
        return redirect('materias')
        
    materias = Materia.objects.all()
    return render(request, 'tutorias/tutor.html', {
        'materias': materias, 
        'tutor': tutor_existente
    })

def es_administrador(user):
    return user.is_staff

@user_passes_test(es_administrador)
def lista_usuarios(request):
    usuarios = User.objects.all().select_related('perfil')
    # Cambiado a lista_users.html para coincidir con tu archivo real en plantillas
    return render(request, 'tutorias/lista_users.html', {'usuarios': usuarios})

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol_seleccionado = request.POST.get('rol', 'estudiante')
            Perfil.objects.create(usuario=user, rol=rol_seleccionado)
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'tutorias/registro.html', {'form': form})

@login_required
def editar_perfil(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user, defaults={'rol': 'estudiante'})
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        if nuevo_rol in ['estudiante', 'tutor']:
            perfil.rol = nuevo_rol
            perfil.save()
            return redirect('inicio')
            
    return render(request, 'tutorias/editar_perfil.html', {'perfil': perfil})


@login_required
def respuestas(request):
    tutor_actual = Tutor.objects.filter(usuario=request.user).first()
    
    consultas_recibidas = []
    if tutor_actual:
        # Traemos las consultas que correspondan a este tutor
        consultas_recibidas = Consulta.objects.filter(tutor=tutor_actual, estado='pendiente')
    
    # 🛠️ LA CLAVE: Traemos todas las materias de la base de datos
    todas_las_materias = Materia.objects.all()
    
    # 🛠️ Enviamos 'materias' en el contexto para que el HTML pueda leerlas
    return render(request, 'tutorias/respuestas.html', {
        'consultas': consultas_recibidas,
        'materias': todas_las_materias  # 👈 Al agregar esto, el select dejará de estar vacío
    })