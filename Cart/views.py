from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CartItem, Cart
from Product.models import Product
from core.errors import HTTPError
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
import json

from User.models import CustomUser as User
from Product.models import Product

@login_required
def cart(request):
    current_user: User = request.user
    
    if not current_user.is_authenticated:
        return HttpResponse("Anda harus masuk untuk melihat keranjang belanja.")
    
    cart, created = Cart.objects.get_or_create(id_user=current_user)
    
    total_harga = CartItem.objects.filter(id_cart=cart).aggregate(total=Sum('subtotal'))['total'] or 0
    print("Total harga:", total_harga) 
    
    cart_items = CartItem.objects.filter(id_cart=cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_harga': total_harga
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
            # Jika item sudah ada dalam keranjang, tingkatkan kuantitas dan hitung ulang subtotal
            cart_item.quantity += 1
            cart_item.subtotal += product.pricePerDay  # Tambahkan harga produk ke subtotal
            cart_item.save()  # Simpan perubahan ke dalam basis data

        else:
            # Jika item baru ditambahkan ke keranjang, hitung subtotal dari harga produk
            cart_item.subtotal = product.pricePerDay
            cart_item.save()  # Simpan item baru ke dalam basis data

        messages.success(
            request, 'Item berhasil ditambahkan ke keranjang belanja.')
        return redirect('Product:list-product')
    except Exception as e:
        return HTTPError().error500(e)
def removeProductFromCart(request, product_id):
    try:
        CartItem.objects.filter(id=product_id).delete()
        messages.success(request, 'Item berhasil dihapus dari keranjang')
        return redirect('Cart:cart')
    except Exception as e:
        return HTTPError().error500(e)
    
def update_quantity(request):
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
                return JsonResponse({'deleted': True})

            # Update quantity
            cart_item.quantity = new_quantity
            cart_item.save()

            # Recalculate subtotal
            cart_item.subtotal = cart_item.id_product.pricePerDay * new_quantity
            cart_item.save()

            subtotal = cart_item.subtotal
            return JsonResponse({'subtotal': subtotal})
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
        