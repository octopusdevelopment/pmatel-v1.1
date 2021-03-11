from django.db import models
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from main.models import Product
from coupons.models import Coupon



class Wilaya(models.Model):
    
    name = models.CharField(max_length=30, verbose_name="Wilaya")
    price = models.DecimalField( max_digits=10, verbose_name="Coût de Livraison", decimal_places=2)
    active = models.BooleanField(default=True, verbose_name="Livraison Active")
    
    class Meta:
        verbose_name = "Wilaya"
        verbose_name_plural = "Wilayas"
        
    def __str__(self):
        return self.name

class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, verbose_name="Wilaya")
    name = models.CharField(max_length=30, verbose_name="Commune")

    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"        
        
    def __str__(self):
        return self.name
    
"""
The coupon is a foreign key that stores the coupon code used, and the discount is the percentage applied with the 
coupon just in case the coupon gets deleted, we will still have a way to retrieve the discount (discount is the amount)
"""


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
    coupon = models.ForeignKey(Coupon, verbose_name="Coupon", related_name='orders', null=True, blank=True, on_delete= models.SET_NULL)
    discount_amount = models.PositiveIntegerField(default=0, validators= [MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ('-created',)
    def __str__(self):
        return f'Commande N°:  {self.id}'
    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost = total_cost - self.discount_amount
        if total_cost < 0:
            total_cost = 0
        return total_cost
    
    def get_total_cost_without_discount(self):
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

