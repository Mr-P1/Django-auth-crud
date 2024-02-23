from django.shortcuts import render,redirect ,get_object_or_404

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate #Es para ver si el usuario esta activo, 

# Create your views here.

from .forms import *
from .models import *

from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'index.html')


def signup(request):
    if request.method=='GET':

        datos = {
            'formulario':UserCreationForm()
        }
        return render(request,'signup.html',datos)
    
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user =User.objects.create_user(username = request.POST['username'], password= request.POST['password1'])
                user.save()

                login(request, user)

                return redirect('tareas')
            
            except:#Usuario ya existe     
                datos = {
                    'formulario':UserCreationForm(),
                    'error':'El usuario ya existe'
                    }

                return render(request,'signup.html',datos)
        
        else: #contraseña distinta
            datos = {
                'formulario':UserCreationForm(),
                'error':'Las contraseñas no son la misma'
                }

            return render(request,'signup.html',datos)
           

def iniciar_sesion(request):

    if request.method == 'GET':
    
    
        datos = {
            'formulario':AuthenticationForm()
        }


        return render(request,'iniciar_sesion.html',datos)
    
    else:

        user = authenticate(request, 
                     username = request.POST['username'],
                     password = request.POST['password'])
        
        if user is None: #No encontro al usuario

            datos = {
                'error':'No se encontro al usuario, verifique el usuario y contraseña',
                'formulario':AuthenticationForm()

            }

            return render(request,'iniciar_sesion.html',datos)

        else:
            login(request, user)

            return redirect('tareas')


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('/')

        
@login_required
def tareas(request):
    tareas = Tarea.objects.filter(usuario = request.user)

    #tareas_compleatadas = Tarea.objects.filter(usuario = request.user, completado__isnull = True) Con esto solo se mostrarian las tareas que no hayan sido completadas

    datos = {
        'tareas':tareas
    }

    return render(request, 'tareas.html',datos)

@login_required
def crear_tareas(request):

    if request.method == 'GET':

        datos = {
            'formulario':TareaFormulario
        }
        return render(request,'create_task.html',datos)
    else:
        try:

        # nuevaTarea = Tarea(titulo = request.POST['titulo'], descripcion = request.POST['descripcion'], importante = request.POST['importante'],usuario_id = request.user_id)
            formulario = TareaFormulario(request.POST)
            nuevaTarea = formulario.save(commit=False) #Esto es para guardar los datos de los campos solamente
            nuevaTarea.usuario = request.user
            nuevaTarea.save()

            return redirect('tareas')
        
        except:
            datos = {
                'error':'Ha ocurrido un error inesperado, intentalo denuevo'
            }

            return render(request,'create_task.html',datos)

@login_required
def detalle_tarea(request, id):
    #tarea = Tarea.objects.get(id = id)

    if request.method == 'GET':
        tarea = get_object_or_404(Tarea,id = id)

        formulario = TareaFormulario(instance= tarea)


       

        return render(request,'tarea_detalle.html',{
            'tarea':tarea,
            'formulario':formulario
        })
    else: #Actualizar datos

        try:
            tarea = get_object_or_404(Tarea,id = id)
            actualizarTarea = TareaFormulario(request.POST, instance=tarea)
            actualizarTarea.save()

            return redirect('tareas')
        
        except : 

            tarea = get_object_or_404(Tarea,id = id)

            formulario = TareaFormulario(instance= tarea)

            return render(request,'tarea_detalle.html',{
            'tarea':tarea,
            'formulario':formulario,
            'error':'ha ocurrido un error, intente denuevo'
        })

#Lo siguiente no lo tome ya que es demasiado extenso
# def completado(request, id):
#     tarea = get_object_or_404(Tarea,id = id)

#     if request.method == 'POST':
#         tarea.completado = timezone.now()
#         tarea.save()
#         return redirect('tareas')


def completado(request, id):

    tarea = get_object_or_404(Tarea,id = id)

    tarea.completado = timezone.now()
    tarea.save()
    return redirect('tareas')


def no_completado(request, id):

    tarea = get_object_or_404(Tarea,id = id)

    tarea.completado = None 
    tarea.save()
    return redirect('tareas')


def eliminar_tarea(request,id):
    tarea = get_object_or_404(Tarea,id = id)

    tarea.delete()
    return redirect('tareas')
