from django.db import models
from django.utils import timezone

from User.models import CustomUser
from Product.models import Product

class Order(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    grand_total = models.BigIntegerField()
    delivery_receipt_code = models.CharField(max_length=255)
    STATUS_CHOICES = (
    ("Unconfirm", "Unconfirm"),
    ("Confirmed", "Confirmed"),
    ("Delivered", "Delivered"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_receipt_image_path = models.TextField()
    address = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order with id : {self.id}"
    
class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE                                                                                                                                                                                                                                          )
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ReturnOrder(models.Model):
    id_return_order = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    return_receipt_code = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")
    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Received', 'Received'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    


