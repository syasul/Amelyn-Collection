from django import forms
from .models import Product

class Productforms(forms.ModelForm):
    class Meta:
        model = Product        
        fields = (
            "name",
            "stock",
            "image",
            "pricePerDay",
            "sizeProduct",
            "description",
            )
