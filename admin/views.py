from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import os


# Product
from Product.models import *

# Order
from Order.models import *

@login_required
def manageProduct(request):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    context = {
        # 'product_form':product_form,
        'title':'manage product',
        'products': Product.objects.all()
    }
    return render(request, 'product/manage_product.html', context)

@login_required
def addProduct(request):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        product_stock = request.POST.get('productStock')
        product_images = request.FILES.get('productImages')
        product_price = request.POST.get('productPrice')
        product_size = request.POST.get('productSize')
        product_desc = request.POST.get('productDesc')

        Product.objects.create(
            name=product_name,
            stock=product_stock,
            image=product_images,
            pricePerDay=product_price,
            sizeProduct=product_size,
            description=product_desc
        )

        return redirect('Admin:manage-product')    
    return redirect('Admin:manage-product')
    

@login_required
def deleteProduct(request, delete_id):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    product = Product.objects.get(id=delete_id)
    os.remove(product.image.path)
    product.delete()
        
    return redirect('Admin:manage-product')

@login_required
def updateProduct(request, update_id):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        product = Product.objects.get(pk=update_id)
        product.name = request.POST.get('productName')
        product.stock = request.POST.get('productStock')
        product.pricePerDay = request.POST.get('productPrice')
        product.sizeProduct = request.POST.get('productSize')
        product.description = request.POST.get('productDesc')

        # Cek apakah gambar produk baru telah diunggah
        if request.FILES.get('productImages'):
            product.images = request.FILES['productImages']

        product.save()


        return redirect('Admin:manage-product')
    else:
        product = Product.objects.get(pk=update_id)
        return render(request, 'product/update_product.html', {'product': product})

@login_required
def searchProduct(request):
    if not request.user.is_superuser:
        return redirect("User:user")
    
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


@login_required
def manageOrder(request):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'order/manageOrder.html', context)

@login_required
def update_status(request, id_order):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order.objects.get(pk=id_order)
        order.status = status
        order.save()
    return redirect('Admin:manage-order')

@login_required
def delete_order(request, id_order):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        order = Order.objects.get(pk=id_order)
        order.delete()
    return redirect('Admin:manage-order')

@login_required
def manageReturnOrder(request):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    returnOrder = ReturnOrder.objects.all()
    context = {
        'returnOrders':returnOrder
    }
    return render(request, 'order/manageReturnOrder.html',context)

@login_required
def updateReturnOrder(request, id_return_order):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        status = request.POST.get('status')
        returnOrder = ReturnOrder.objects.get(id_return_order=id_return_order)
        returnOrder.status = status
        returnOrder.save()
    return redirect('Admin:manage-return-order')

@login_required
def deleteReturnOrder(request, id_return_order):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        returnOrder = ReturnOrder.objects.get(id_return_order=id_return_order)
        returnOrder.delete()
    return redirect('Admin:manage-return-order')
    
@login_required
def manageTestimonial(request):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    testimonial = Testimonial.objects.all()
    context = {
        'testimonials':testimonial
    }
    return render(request, 'order/manageTestimonial.html',context)

@login_required
def deleteTesimonial(request, id_testimonial):
    if not request.user.is_superuser:
        return redirect("User:user")
    
    if request.method == 'POST':
        testimonial = Testimonial.objects.get(id_testimonial=id_testimonial)
        testimonial.delete()
    return redirect('Admin:manage-testimonial')
