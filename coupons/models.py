from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from decimal import Decimal


class Coupon(models.Model):
    '''
    DESCRIPTION:
    Code: The code that users have to enter in order to apply the coupon to their
    purchase
    valid_from: datetime value - when coupon becomes valid
    valid_to: datetime value - when coupon becomes invalid
    discount: discount rate to apply, minimum is 0, maximum is 100
    active: indicates whether the coupon is active
    '''
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(verbose_name='Valide à partir de', null=False, blank=False)
    valid_to = models.DateTimeField('Valide jusqu\'à', null=False, blank=False)
    discount_amount = models.IntegerField(verbose_name='Montant' , validators= [MinValueValidator(0)], default= 0)
    discount_percentage = models.IntegerField(verbose_name= 'Pourcentage',  validators= [MinValueValidator(0), MaxValueValidator(100)], default=0)
    active = models.BooleanField(verbose_name='actif')
    stock = models.IntegerField(verbose_name = 'Coupons restant', validators= [MinValueValidator(0)], default= 3)
    
    
    # In the admin side this method will check if the values are 0 together or both set
    def clean(self):
      
        if (self.discount_amount == 0) & (self.discount_percentage == 0):
                raise ValidationError("Le pourcentage ou le montant doivent être différents de zéro, pas les deux en même temps")
        if (self.discount_amount > 0) & (self.discount_percentage > 0):
                raise ValidationError('Le pourcentage ou le montant doivent être différents à 0, pas les deux en même temps')

        if(self.valid_from >= self.valid_to):
                raise ValidationError("La date de fin doit être plus récente que la date de début")
            
    class Meta:
        verbose_name: 'Coupon'
        ordering = ('-valid_from', '-valid_to')
    

    def __str__(self):
        return self.code
    
    