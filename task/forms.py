from django import forms
from .models import * 


class TareaFormulario(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo','descripcion','importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa un titulo'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','placeholder':'Ingresa una descripcion'}),
           'importante': forms.CheckboxInput(attrs={'class':'form-check-input text-center'})
        }