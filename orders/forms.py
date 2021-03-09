from django import forms
from .models import Order, Wilaya, Commune

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'addresse', 'email', 'phone', 'wilaya', 'commune', 'note']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        