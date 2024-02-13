from django.db import models


class Product(models.Model):

    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images/")
    pricePerDay = models.IntegerField()
    sizeProduct = models.CharField(max_length=2, choices=SIZE_CHOICES)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}. {}".format(self.id, self.name)



