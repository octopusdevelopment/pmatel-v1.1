from decimal import Decimal
from django.conf import settings
from main.models import Product
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        
        #get the current cart 
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
        #get current applied coupon
        self.coupon_id = self.session.get('coupon_id') 


        """
    This method is defined as a property. If the cart contains 
    a coupon_id attribute, the Coupon object with the given ID is returned.
    """
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id, stock__gt=0)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def add_one(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        # The old quantity will not be deleted
        self.cart[product_id]['quantity'] += quantity 
        self.save()


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        self.cart[product_id]['quantity'] = quantity
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            desired_quantity = cart[str(product.id)]['quantity']
            removed = False
            if product.stock == 0:
                self.remove(product)
                removed = True
            elif product.available == False & removed == False:
                self.remove(product)
            else:
                if product.stock > desired_quantity:
                    quantity = desired_quantity
                elif product.stock < desired_quantity & product.stock > 10:
                    quantity = 5
                else:
                    quantity = 1
                cart[str(product.id)]['product'] = product
                cart[str(product.id)]['quantity'] = quantity
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item



    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values() )

    # discount = total price * coupon discount
    def get_discount(self):
        if self.coupon:
            if self.coupon.discount_amount:
                return self.coupon.discount_amount
            else:
                return (self.coupon.discount_percentage / Decimal(100)) \
                * self.get_total_price()
                
        return Decimal(0)

    # total price after discount = total price - discount price
    
    def get_total_price_after_discount(self):
        price = self.get_total_price() - self.get_discount()
        if price < 0:
            price = 0
        return price
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()