# Put your utils functions here
from .models import Product
from decimal import Decimal


"""
This method is used when the user purchases directly a product       
"""     
def get_discount(product, coupon):
    if coupon:
            if coupon.discount_amount:
                return coupon.discount_amount
            else:
                return coupon.discount_percentage / Decimal(100) \
                * product.price
                
    return Decimal(0)
    

def manage_quantity(product, quantity):
    
    desired_quantity = quantity
    print('INSIDE MANAGE QUANTITY')
    print(product, product.stock, desired_quantity)
    try:
        if product.stock > desired_quantity:
                quantity = desired_quantity
        elif product.stock < desired_quantity & product.stock > 10:
                quantity = 5
        else:
                quantity = 1
        success = True
    except Exception:
        print(Exception)
        quantity = 0
        success = False
        
    return {"quantity": quantity, "success": success}