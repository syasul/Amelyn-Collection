from django.db import models
from django.contrib.auth.models import User

from .models import Product

# Create your models here.
class Cart(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart {self.id_cart} - User: {self.user.username}"
    

class CartItem(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    
    def __str__(self):
        return f"Item {self.id_cartitem} - Product: {self.product.name} - Quantity: {self.quantity} - Subtotal: {self.subtotal}"

    
