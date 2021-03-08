from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime
from django.db.models import F
from django.conf import settings
import os
from django.utils.deconstruct import deconstructible


from ckeditor.fields import RichTextField
# Create your models here.

# CATEGORIES = (
#     ('PT','Postes Téléphoniques'),
#     ('ST','Standards Téléphoniques'),
#     ('IV','Interphones et Vidéophones'),
#     ('SS', 'Systèmes de Sécurité')
# )

PRODUCT_STATUS = (
    ('N', 'Nouveau'),
    ('P', 'Promotion'),
    ('S', 'Sans Status')
)

@deconstructible
class PathAndRename(object):
   def __init__(self, sub_path):
       self.path = sub_path

   def __call__(self, instance, filename):
       
       filename = 'product_{0}_{1}'.format(instance.user.id, filename)
       # return the whole path to the file
       return os.path.join(self.path, filename)

def solution_directory_path(instance, filename):
    date_fields = str(datetime.date.today()).split('-')
    year = date_fields[0]
    month = date_fields[1]
    day = date_fields[2]
    
    # file will be uploaded to MEDIA_ROOT/solutions/YEAR/MONTH/DAY/solution_id_<filename>
    solution_sub_path = 'solutions/{0}/{1}/{2}/solution_{3}_{4}'.format(year, month, day, instance.id, filename)
    solution_full_path = os.path.join(settings.MEDIA_ROOT, solution_sub_path)
    if os.path.exists(solution_full_path):
        os.remove(solution_full_path)
    return solution_sub_path

def product_directory_path(instance, filename):
    
    date_fields = str(datetime.date.today()).split('-')
    year = date_fields[0]
    month = date_fields[1]
    day = date_fields[2]
    
    # file will be uploaded to MEDIA_ROOT/produits/YEAR/MONTH/DAY/produit_<produit_id>_<filename>
    product_sub_path = 'produits/{0}/{1}/{2}/product_{3}_{4}'.format(year, month, day,instance.product_id, filename)
    product_full_path = os.path.join(settings.MEDIA_ROOT, product_sub_path)
    if os.path.exists(product_full_path):
        os.remove(product_full_path)
    return product_sub_path


class Solution(models.Model):
    name         = models.CharField( max_length=50)
    slug        = models.SlugField( max_length=70) 
    photo       = models.ImageField(verbose_name='Photo de la solution', upload_to=solution_directory_path, blank=True)
    photo_2     = models.ImageField(verbose_name='Photo 2 de la solution', upload_to=solution_directory_path, blank= True)
    description = RichTextField(verbose_name='Text en plus', blank= True, null=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("produit", args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("product-by-cat", args = [self.slug])
    

class Product(models.Model):
    
    product_id  = models.CharField(max_length= 50, blank=False, null= False, unique=True, default='',verbose_name='Numéro du Produit')
    name        = models.CharField(max_length=50, verbose_name = 'Nom du Produit', db_index=True)
    slug        = models.SlugField(max_length=70, verbose_name= 'Slug')
    solution    = models.ForeignKey(Solution, on_delete=models.SET_NULL, verbose_name='Solution', default='', null=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, verbose_name='Catégorie')
    sub_title  = models.CharField(max_length=100, verbose_name=("Sous titre"), blank= True)
    description = RichTextField(verbose_name='Texte en Plus', blank= True, null=True)
    sup_info    = RichTextField(verbose_name='Informations Supplémentaires', blank= True, null=True)
    photo       = models.ImageField(verbose_name='Photo du Produit', upload_to= product_directory_path, blank=True)
    photo_2     = models.ImageField(verbose_name='Photo du Produit 2', upload_to= product_directory_path, blank=True)
    file_1   = models.FileField(verbose_name='Fichier 1', upload_to='fichiers/', blank= True)
    price = models.DecimalField(verbose_name='Prix', max_digits=10, decimal_places=2)
    available = models.BooleanField(verbose_name='Disponibilité', default=True)
    status = models.CharField(choices= PRODUCT_STATUS, max_length=50, default='S' , blank=False, null = False, verbose_name="Status")
    created = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("details-produit", args=[self.slug])
    
        class Meta:
            ordering = ('name',)
            verbose_name = 'Produit'
            verbose_name_plural = 'Produits'



DEPARTEMENT_CHOICES=[
    ('C', 'Commercial'),
    ('D', 'Direction'),
    ('M', 'Marketing'),
    ('SC', 'Service client'),
    ]

class ContactForm(models.Model):
    name        = models.CharField(max_length=50)
    departement = models.CharField(max_length=2, choices=DEPARTEMENT_CHOICES, default='D',)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20)
    subject     = models.CharField(max_length=50)
    fichier     = models.FileField(upload_to='fichiers/% d/% m/% Y/', max_length=20, blank=True)
    message     = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Formulaire de contact'





class Post(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    intro = models.CharField(max_length=200, blank=True)
    image = models.ImageField(verbose_name='Image' ,upload_to='slides/', blank= True)
    text = RichTextField(verbose_name='Article', blank= True, null=True)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.titre



