
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]


class DateInput(forms.ModelForm):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ['subject','title','description','is_finished']



class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title','is_completed']


class DashForm(forms.Form):
    text = forms.CharField(max_length=100,label="Search Videos on youtube: ")


class ConversionForm(forms.Form):
    CHOICES = [('length','length'),('mass','mass')]
    measurement = forms.ChoiceField(choices = CHOICES,widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','yard'),('foot','foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number',"placeholder":'Enter the number'}
    ))

    measure1 = forms.CharField(
        label='',widget=forms.Select(choices = CHOICES)
        )

    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )


class ConversionMassForm(forms.Form):
    CHOICES = [('pound','pound'),('kilogram','kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number',"placeholder":'Enter the number'}
    ))

    measure1 = forms.CharField(
        label='',widget=forms.Select(choices = CHOICES)
        )

    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )