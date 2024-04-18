from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import os

# Product
from Product.models import *
from Product.forms import *

# Order
from Order.models import *



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
        
        return redirect('Admin:manage-product')
    context = {
        'title':'add product',
        'product_form':product_form
    } 
    
    return render(request,'product/add_product.html', context)

def deleteProduct(request, delete_id):
    
    product = Product.objects.get(id=delete_id)
    os.remove(product.image.path)
    product.delete()
        
    return redirect('Admin:manage-product')

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

        return redirect('Admin:manage-product')
    
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

    return HttpResponseRedirect(reverse('Admin:manage-product'))


def manageOrder(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'order/manageOrder.html', context)

def update_status(request, id_order):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order.objects.get(pk=id_order)
        order.status = status
        order.save()
    return redirect('Admin:manage-order')

def delete_order(request, id_order):
    if request.method == 'POST':
        order = Order.objects.get(pk=id_order)
        order.delete()
    return redirect('Admin:manage-order')

def manageReturnOrder(request):
    returnOrder = ReturnOrder.objects.all()
    context = {
        'returnOrders':returnOrder
    }
    return render(request, 'order/manageReturnOrder.html',context)

def updateReturnOrder(request, id_return_order):
    if request.method == 'POST':
        status = request.POST.get('status')
        returnOrder = ReturnOrder.objects.get(id_return_order=id_return_order)
        returnOrder.status = status
        returnOrder.save()
    return redirect('Admin:manage-return-order')

def deleteReturnOrder(request, id_return_order):
    if request.method == 'POST':
        returnOrder = ReturnOrder.objects.get(id_return_order=id_return_order)
        returnOrder.delete()
    return redirect('Admin:manage-return-order')
    
def manageTestimonial(request):
    testimonial = Testimonial.objects.all()
    context = {
        'testimonials':testimonial
    }
    return render(request, 'order/manageTestimonial.html',context)

def deleteTesimonial(request, id_testimonial):
    if request.method == 'POST':
        testimonial = Testimonial.objects.get(id_testimonial=id_testimonial)
        testimonial.delete()
    return redirect('Admin:manage-testimonial')
