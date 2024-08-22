from django import forms
from .models import *

class BusquedaPruebaForm(forms.Form):
    numero_ficha = forms.CharField(max_length=10, required=True, label='Número de Ficha')
    numero_documento = forms.IntegerField(required=True, label='Número de Documento')


# Formulario para la Prueba (Evaluación)
class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['ficha']
        labels = {
            'ficha': 'Seleccione la ficha para la prueba',
        }
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ficha'].queryset = Ficha.objects.all()
        self.fields['ficha'].label_from_instance = lambda obj: f'Ficha {obj.numero}'

# Formulario para las Preguntas de la Prueba
class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto_pregunta', 'prueba']
        labels = {
            'texto_pregunta': 'Ingrese la pregunta',
            'prueba': 'Seleccione la prueba',
        }
        widgets = {
            'texto_pregunta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el texto de la pregunta'}),
            'prueba': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para las Respuestas de los Aprendices
class RespuestaPreguntaForm(forms.ModelForm):
    class Meta:
        model = RespuestaPregunta
        fields = ['texto_respuesta', 'pregunta', 'aprendiz', 'instructor']
        labels = {
            'texto_respuesta': 'Respuesta del aprendiz',
            'pregunta': 'Pregunta relacionada',
            'aprendiz': 'Seleccione el aprendiz',
            'instructor': 'Seleccione el instructor',
        }
        widgets = {
            'texto_respuesta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la respuesta'}),
            'pregunta': forms.Select(attrs={'class': 'form-control'}),
            'aprendiz': forms.Select(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
        }
