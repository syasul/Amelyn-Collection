from django.db import models
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator
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
    payment_receipt_image_path = models.ImageField(upload_to="images/")
    address = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fine = models.BigIntegerField(default=0)
    
    def hitung_fine(self):
        if self.status == 'Delivered':
            if self.end_date < timezone.now().date():
                hari_keterlambatan = (timezone.now().date() - self.end_date).days
                if hari_keterlambatan > 0:
                    self.fine = (self.grand_total * 0.02) * hari_keterlambatan
                else:
                    self.fine = 0
            else:
                self.fine = 0
        else:
            self.fine = 0

    def save(self, *args, **kwargs):
        self.hitung_fine()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order with id : {self.id}"
    
class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ReturnOrder(models.Model):
    id_return_order = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    return_receipt_code = models.ImageField(upload_to="images/")
    image = models.ImageField(upload_to="images/")
    photo_payment_fine = models.ImageField(upload_to='images/', null=True, blank=True)
    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Received', 'Received'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sent')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.id_order.fine > 0:
            if not self.photo_payment_fine:
                raise ValueError("Foto pembayaran denda wajib diunggah untuk pengembalian terlambat")
        super().save(*args, **kwargs)


    
class Testimonial(models.Model):
    id_testimonial = models.AutoField(primary_key=True, unique=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)