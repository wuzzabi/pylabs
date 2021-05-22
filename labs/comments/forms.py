from django import forms

from .models import *

class SortForm(forms.ModelForm):
    #Форма отзывов
    class Meta:
        model = ServMonitor
        fields = ('name',)
