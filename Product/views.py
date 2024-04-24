from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
import os

def listProduct(request):
     context = {
          'products':Product.objects.all(),
          'title': 'list product'
     }
     return render(request, 'product/list_product.html', context)

def detailProduct(request, detail_id):
    product = Product.objects.get(id=detail_id)
    
    context = {
        "products":product
    }

    return render(request,'product/detail_product.html', context)
