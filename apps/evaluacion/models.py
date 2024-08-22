from django.db import models
from ..usuario.models import Usuario

class Instructor(models.Model):
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Ficha(models.Model):
    numero = models.CharField('Digite el numero de ficha', max_length=10, blank=False, null=False)
    instructores = models.ManyToManyField(Instructor)
    aprendices = models.ManyToManyField(Usuario)
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' Instructores {self.instructores.count()} - Aprendices {self.aprendices.count()}'

class Prueba(models.Model):
    ficha = models.OneToOneField(Ficha, null=True, on_delete=models.SET_NULL)  # Una única prueba por ficha
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default = True)

    def __str__(self):
        return f'Prueba para ficha {self.ficha.id} - {self.fecha_creacion}'

class Pregunta(models.Model):
    texto_pregunta = models.CharField('Digite una pregunta', max_length=200, blank=False, null=False)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)  # Preguntas asociadas a la prueba

    def __str__(self):
        return f'Pregunta: {self.texto_pregunta}'

class RespuestaPregunta(models.Model):
    texto_respuesta = models.CharField('Digite su respuesta', max_length=200, blank=False, null=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)  # Relación con la pregunta
    aprendiz = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Quién responde
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)  # A qué instructor se refiere la respuesta

    def __str__(self):
        return f'Respuesta: {self.texto_respuesta} del aprendiz {self.aprendiz} al instructor {self.instructor}'


