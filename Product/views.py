from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
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

def manageProduct(request):
    context = {
        'title':'manage product',
        'products': Product.objects.all()
    }
    return render(request, 'product/manage_product.html', context)

def addProduct(request):
    product_form = Productforms(request.POST or None , request.FILES or None )
    if request.method == 'POST':
        if product_form.is_valid():
            product_form.save()
        
        return redirect('Product:manage-product')
    context = {
        'title':'add product',
        'product_form':product_form
    } 
    
    return render(request,'product/add_product.html', context)

def deleteProduct(request, delete_id):
    
    product = Product.objects.get(id=delete_id)
    os.remove(product.image.path)
    product.delete()
        
    return redirect('Product:manage-product')

def updateProduct(request, update_id):
    product_update = Product.objects.get(id=update_id)

    data = {

        'name': product_update.name,
        'stock' : product_update.stock,
        'pricePerDay': product_update.pricePerDay,
        'sizeProduct': product_update.sizeProduct,
        'description': product_update.description,
    }

    product_form = Productforms(request.POST or None, request.FILES or None, initial=data, instance=product_update)
    if request.method == 'POST':
        if product_form.is_valid():
            image_path = product_update.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
            product_form.save()

        return redirect('Product:manage-product')
    
    context = {

        'title':'update product',
        'product_form':product_form,
        'update':product_update 
    }
    
    return render(request,'product/add_product.html', context)

def searchProduct(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        searched = searched.strip()
        product = Product.objects.filter(name__icontains=searched)

        context = {
            'searched': searched,
            'products': product,
        }

        return render(request, 'product/search_product.html', context)

    return HttpResponseRedirect(reverse('Product:manage-product'))