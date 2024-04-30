from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db.models import Q
import os

from .utils import currency

def listProduct(request):
    current_user = request.user
    query = request.GET.get('q')

    products = Product.objects.all()
    for product in products:
        product.pricePerDay = currency(product.pricePerDay)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'products': products,
        'title': 'list product',
        'current_user':current_user
    }

    return render(request, 'product/list_product.html', context)

def detailProduct(request, detail_id):
    current_user = request.user
    product = Product.objects.get(id=detail_id)
    product.pricePerDay = currency(product.pricePerDay)
    
    context = {
        'current_user': current_user,
        "products":product
    }

    return render(request,'product/detail_product.html', context)
