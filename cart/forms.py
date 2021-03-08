from django import forms 
from django.forms import NumberInput
from django.core import validators



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField( min_value=1, widget=NumberInput(attrs={'class': 'form-control text-center','value': 1, 'max':20 }))
   