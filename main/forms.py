from django import forms
from .models import ContactForm

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name','phone','email','subject','message',]

class SearchForm(forms.Form):
    query = forms.CharField()

class HomeProductSeachForm(forms.Form):
    product = forms.CharField(required=False)
    category = forms.CharField(required=False)
    status = forms.CharField(required=False)