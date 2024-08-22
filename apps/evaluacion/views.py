from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
from django.contrib import messages
from .models import *
from .forms import *

#INDEX EVALUACION INSTRUCTORES 
def inicio(request):
    return render(request, 'index.html')

def evaluacionHome(request):
    return render(request, 'evaluacionHome.html')
#CRUD PRUEBA
def crear_prueba(request):
    if request.method == "POST":
        form = PruebaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_prueba', prueba_id=form.instance.id)
    else:
        form = PruebaForm()
    return render(request, 'evaluacion/prueba/crear_prueba.html',{'form':form})

def eliminar_prueba(request, prueba_id):
    prueba = get_object_or_404(Prueba, pk=prueba_id)

    if request.method == "POST":
        prueba.delete()
        return redirect('evaluacionHome')
    
    # Si el método es GET, podrías mostrar una confirmación o redirigir
    return render(request, 'evaluacion/prueba/prueba_confirm_delete.html', {'prueba': prueba})
    
def listar_pruebas(request):
    prueba = Prueba.objects.all()
    return render(request, 'evaluacion/prueba/listar_pruebas.html',{'form' :prueba})    

def carga_masiva(request):
    if request.method == "POST":
        # Proceso de carga de preguntas
        if 'file_preguntas' in request.FILES:
            archivo_preguntas = request.FILES['file_preguntas']
            try:
                # Cargar el archivo Excel
                df_preguntas = pd.read_excel(archivo_preguntas, engine='openpyxl')
                
                for _, row in df_preguntas.iterrows():
                    prueba_id = row['prueba']
                    
                    # Intentar obtener la prueba
                    try:
                        prueba = Prueba.objects.get(id=prueba_id)
                    except Prueba.DoesNotExist:
                        messages.error(request, f"Prueba con ID {prueba_id} no existe. Fila omitida.")
                        continue  # Saltar a la siguiente fila si la prueba no existe
                    
                    # Verificar si la pregunta ya existe para esa prueba
                    if not Pregunta.objects.filter(texto_pregunta=row['texto_pregunta'], prueba=prueba).exists():
                        # Crear la nueva pregunta asociada a la prueba
                        Pregunta.objects.create(texto_pregunta=row['texto_pregunta'], prueba=prueba)
                
                messages.success(request, "Preguntas cargadas exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al cargar preguntas: {str(e)}")
        
        # Proceso de carga de instructores
        # ...

        # Proceso de carga de aprendices
        # ...

        return redirect('carga_masiva')
    
    return render(request, 'evaluacion/prueba/carga_masiva.html')

def evaluacion_home(request):
    form = BusquedaPruebaForm()
    prueba = None
    mensaje_error = None
    
    if request.method == 'POST':
        form = BusquedaPruebaForm(request.POST)
        if form.is_valid():
            numero_ficha = form.cleaned_data['numero_ficha']
            numero_documento = form.cleaned_data['numero_documento']
            
            try:
                usuario = Usuario.objects.get(numeroDocumento=numero_documento, usuario_activo=True)
                ficha = Ficha.objects.get(numero=numero_ficha, aprendices=usuario)
                
                prueba = Prueba.objects.filter(ficha=ficha, activa=True).first()
                
                if not prueba:
                    mensaje_error = 'No se encontró una prueba activa para esta ficha.'
            except Usuario.DoesNotExist:
                mensaje_error = 'El usuario no existe o no está activo.'
            except Ficha.DoesNotExist:
                mensaje_error = 'No se encontró una ficha con el número proporcionado.'
    
    context = {
        'form': form,
        'prueba': prueba,
        'mensaje_error': mensaje_error,
    }
    return render(request, 'evaluacionHome.html', context)