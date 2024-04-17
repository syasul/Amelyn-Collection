from django import forms
from .models import *

class ReturnOrderforms(forms.ModelForm):
    class Meta:
        model =  ReturnOrder       
        fields = (
            "return_receipt_code",
            "image",
            )

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = (
            "content",
        )