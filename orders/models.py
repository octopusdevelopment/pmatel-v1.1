from django.db import models
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from main.models import Product



class Wilaya(models.Model):
    
    name = models.CharField(max_length=30, verbose_name="Wilaya")
    price = models.DecimalField( max_digits=10, verbose_name="Coût de Livraison", decimal_places=2)
    active = models.BooleanField(default=True, verbose_name="Livraison Active")
    def __str__(self):
        return self.name

class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, verbose_name="Wilaya")
    name = models.CharField(max_length=30, verbose_name="Commune")

    def __str__(self):
        return self.name
    

class Order(models.Model):
 
    first_name  = models.CharField(verbose_name="Prénom" , max_length=50)
    last_name   = models.CharField(verbose_name="Nom" , max_length=50)
    addresse    = models.CharField(verbose_name="Adresse" , max_length=250)
    phone       = models.CharField(verbose_name="Téléphone" , max_length=25)
    email       = models.EmailField(verbose_name="Email", null=True, blank = True)
    wilaya      = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True)
    commune     = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True, verbose_name="Créée")
    updated     = models.DateTimeField(auto_now=True, verbose_name= "Modifiée")
    note        = models.TextField(verbose_name= "Note", blank=True, null=True)
    paid        = models.BooleanField(default=False, verbose_name="Payée")
    confirmed   = models.BooleanField(default=False, verbose_name="Confirmée")
    
    class Meta:
        verbose_name = "Commande"
        ordering = ('-created',)
    def __str__(self):
        return f'Commande N°:  {self.id}'
    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost
    
    
class OrderItem(models.Model):
    order    = models.ForeignKey(Order,related_name='items', verbose_name=("Commande"), on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, verbose_name=("Commande"), on_delete=models.CASCADE)
    price    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    quantity = models.PositiveIntegerField(default = 1, verbose_name="Quantité" )
    
    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity

