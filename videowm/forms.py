from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.forms import ModelForm
from models import *

class WebminarForm(ModelForm):
    class Meta:
        model = Webminar
        widgets = {
            'inicio' : DateTimePicker(),
            'fin' : DateTimePicker()
        }

class MensajeForm(ModelForm):
    class Meta:
        model = Mensaje
