from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import F


from ckeditor.fields import RichTextField
# Create your models here.

CATEGORY_CHOICES=[
    ('IN', 'Intrusion'),
    ('IC', 'Incendie Conventionnelle'),
    ('IA', 'Incendie Adressable'),
    ]


class Produit(models.Model):

    # ordre       = models.IntegerField(blank=True, null=True)
    name        = models.CharField( max_length=50)
    slug        = models.SlugField( max_length=70)
    category    = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='IN')
    sous_titre  = models.CharField(max_length=100, verbose_name=("Sous titre"), blank= True)
    description = RichTextField(verbose_name='Text en plus', blank= True, null=True)
    info_sup    = RichTextField(verbose_name='informations suplaimentaires', blank= True, null=True)
    photo       = models.ImageField(verbose_name='Photo du produit', upload_to='produits/')
    photo_2     = models.ImageField(verbose_name='Photo du produit 2', upload_to='produits/', blank= True)
    fichier_1   = models.FileField(verbose_name='fichier 1', upload_to='fichiers/', blank= True)
    fichier_2   = models.FileField(verbose_name='fichier 2', upload_to='fichiers/', blank= True)
    fichier_3   = models.FileField(verbose_name='fichier 3', upload_to='fichiers/', blank= True)
    fichier_4   = models.FileField(verbose_name='fichier 4', upload_to='fichiers/', blank= True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produits'
        verbose_name_plural = 'Produits'



class Slide(models.Model):
    title = models.CharField(verbose_name='titre' ,max_length= 200, blank = True)
    image = models.ImageField(upload_to= 'slides/')
    class Meta:
        verbose_name = "Photo page d'accueil"
        verbose_name_plural = "Photos page d'accueil"



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



