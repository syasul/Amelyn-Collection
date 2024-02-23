from django.db import models
# from django.contrib.auth.models import User

from Product.models import Product
from User.models import CustomUser

# Create your models here.
class Cart(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart for User with id : {self.id_user}"
    

class CartItem(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Item {self.id_cartitem} - Product: {self.product.name} - Quantity: {self.quantity} - Subtotal: {self.subtotal}"

    
