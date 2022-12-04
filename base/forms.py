from logging import getLogger

from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, Textarea, ModelForm

from base.models import Room

LOGGER = getLogger()


# class RoomForm(Form):
# name = forms.CharField(max_length=200, validators=[muj_validator]) #validator - ruční validace - musí být funkce muj_validator
# description = forms.CharField(widget=Textarea, required=False)
# def muj_validator(value):
#     msmhkiojoijojo    (if neco, tak neco)
#         raise neco - musí tam být ta možnost vyhození výjimky, když je něco špatně

# toto FormView - nasledujici pro typ CreateView

# vyřeší tento ModelForm i duplicitu - typu tato mistnost uz existuje, muzeme i vlastni popisky, ale to se musi resit rucne, automaticke hlasky muzeme prebarvovat, umistit jinam atd.
# další způsob validace je metoca clean (tam se dá případně ten return ještě upravit - například return name.upper

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            validation_error = "Name must contains min. 2 characters."
            LOGGER.warning(f'{name} : {validation_error}')
            raise ValidationError(validation_error)
        return name
