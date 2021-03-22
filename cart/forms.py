from django import forms 
from django.forms import NumberInput
from django.core import validators
from main.models import Product



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField( min_value=1, widget=NumberInput(attrs={'class': 'form-control text-center','value': 1, 'max':20 }))

class CartAddProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)