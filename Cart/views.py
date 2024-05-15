from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from core.errors import HTTPError
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
import json

from User.models import CustomUser as User
from .models import CartItem, Cart
from Product.models import Product

from .utils import currency

@login_required
def cart(request):
    current_user: User = request.user
    
    if not current_user.is_authenticated:
        return HttpResponse("Anda harus masuk untuk melihat keranjang belanja.")
    
    cart, created = Cart.objects.get_or_create(id_user=current_user)
    
    total_harga = CartItem.objects.filter(id_cart=cart).aggregate(total=Sum('subtotal'))['total'] or 0
    total_harga = currency(total_harga)
    
    cart_items = CartItem.objects.filter(id_cart=cart)
    for cart_item in cart_items:
        cart_item.id_product.pricePerDay = currency(cart_item.id_product.pricePerDay)
        cart_item.subtotal = currency(cart_item.subtotal)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_harga': total_harga,
        'current_user': current_user
    }
    
    return render(request, 'cart/cart.html', context)
    
@login_required
def addToCart(request, product_id):
    try:
        current_user = request.user

        if not current_user.is_authenticated:
            messages.warning(request, "Anda harus masuk untuk menambahkan item ke keranjang belanja.")
            return redirect('Product:list-product')

        product = Product.objects.get(id=product_id)

        cart, created = Cart.objects.get_or_create(id_user=current_user)

        cart_item, created = CartItem.objects.get_or_create(id_cart=cart, id_product=product)

        if not created:
            # Jika item sudah ada di keranjang, tambahkan satu ke jumlahnya
            cart_item.quantity += 1

        # Update subtotal dengan harga produk per hari dikali jumlah
        cart_item.subtotal = product.pricePerDay * cart_item.quantity
        cart_item.save()

        # Calculate the total harga for the cart
        total_harga = CartItem.objects.filter(id_cart=cart).aggregate(total=Sum('subtotal'))['total'] or 0

        messages.success(request, 'Item berhasil ditambahkan ke keranjang belanja.')
        return redirect('Product:list-product')
    except Exception as e:
        # Gunakan HttpResponse untuk menampilkan pesan kesalahan yang lebih spesifik
        return HttpResponse("Terjadi kesalahan: " + str(e))
    
def removeProductFromCart(request, product_id):
    try:
        CartItem.objects.filter(id=product_id).delete()
        messages.success(request, 'Item berhasil dihapus dari keranjang')
        return redirect('Cart:cart')
    except Exception as e:
        return HTTPError().error500(e)

@require_POST
def update_quantity(request):
    current_user = request.user
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            new_quantity = int(data.get('new_quantity'))
            if not item_id or new_quantity is None:
                raise ValueError('Item ID and new quantity are required')
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)

        try:
            cart_item = CartItem.objects.get(id=item_id)
            if new_quantity == 0:
                cart_item.delete()
                cart_items = CartItem.objects.filter(id_cart=cart_item.id_cart)
                total_harga = sum([item.subtotal for item in cart_items])
                return JsonResponse({'deleted': True, 'total_harga': total_harga})

            # Update quantity
            cart_item.quantity = new_quantity
            cart_item.save()

            # Recalculate subtotal
            cart_item.subtotal = cart_item.id_product.pricePerDay * new_quantity
            cart_item.save()

            # Recalculate total harga
            cart, created = Cart.objects.get_or_create(id_user=current_user)
            total_harga = CartItem.objects.filter(id_cart=cart).aggregate(total=Sum('subtotal'))['total'] or 0

            return JsonResponse({'subtotal': cart_item.subtotal, 'total_harga': total_harga})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    
    
@require_POST
def remove_product(request):
    item_id = request.POST.get('item_id')

    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        return JsonResponse({'deleted': True})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        