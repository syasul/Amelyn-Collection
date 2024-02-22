from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import CartItem
from Product.models import Product

@login_required
def Cart(request):
    current_user = request.user
    
    if not current_user.is_authenticated:
        return HttpResponse("Anda harus masuk untuk melihat keranjang belanja.")
    
    cart, created = Cart.objects.get_or_create(id_user=current_user)
    
    cart_items = CartItem.objects.filter(id_cart=cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    
    return render(request, 'cart/cart.html', context)
    
@login_required
def addToCart(request, product_id):
    try:
        current_user = request.user
    
        if not current_user.is_authenticated:
            return HttpResponse("Anda harus masuk untuk menambahkan item ke keranjang belanja.")
    
        product = Product.objects.get(id=product_id)
        
        cart, created = Cart.objects.get_or_create(id_user=current_user)
        
        cart_item, created = CartItem.objects.get_or_create(id_cart=cart, id_product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.subtotal += product.price
            cart_item.save()
        
        return redirect('Product:list-product')
    except Exception as e:
        print("erro", e)
    


def removeMenuFromCart(product_id):
    return redirect('Cart:cart')
    
    