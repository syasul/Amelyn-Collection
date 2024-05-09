from django.shortcuts import render

# testimonials
from Order.models import Testimonial

# product
from Product.models import Product

from .utils import currency

def userView(request):
    current_user = request.user
    testimonials = Testimonial.objects.all().order_by('-created_at')[:6]
    products = Product.objects.all().order_by('-created_at')[:6]
    for product in products:
        product.pricePerDay = currency(product.pricePerDay)
        
    return render(request, 'user/user.html', {'current_user':current_user, 'testimonials': testimonials, 'products':products})

def contactView(request):
    return render(request, 'user/contactUs.html')


