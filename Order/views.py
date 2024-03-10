from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.db.models import Sum
from datetime import datetime

from .models import Order, OrderItem
from User.models import CustomUser as User
from Cart.models import Cart, CartItem

# Create your views here.
@login_required
def checkoutForm(request):
    userEmail = None
    if request.user.is_authenticated:
        userEmail = request.user.email
        
    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        start_date = request.POST.get('checkIn')
        end_date = request.POST.get('checkOut')
        telephone = request.POST.get('telephone')
        address = request.POST.get('address')
        
        # Validasi tanggal check-in harus minimal hari ini dan harus lebih awal daripada check-out
        if start_date < timezone.now().strftime('%Y-%m-%d'):
            messages.error(request, "Check-in date cannot be in the past.")
            return HttpResponseBadRequest("Invalid Check-in Date")

        if end_date <= start_date:
            messages.error(request, "Check-out date must be after check-in date.")
            return HttpResponseBadRequest("Invalid Check-out Date")
        
        current_user = request.user
        
        request.session['checkout_data'] = {
            'id_user': current_user.id,
            'start_date': start_date,
            'end_date': end_date,
            'address': address
        }
        return redirect("Order:paymentOrder")
        
    return render(request, 'order/formCheckout.html', { 'user_email': userEmail })


@login_required
def paymentOrder(request):
    current_user = request.user
    checkout_data = request.session.get('checkout_data')
    order = None
    grand_total = None
    order_items = None

    if not current_user.is_authenticated:
        return HttpResponse("Anda harus masuk untuk melihat keranjang belanja.")

    # Pemrosesan data keranjang belanja
    cart = Cart.objects.get_or_create(id_user=current_user)[0]
    cart_items = CartItem.objects.filter(id_cart=cart)
    total_harga = cart_items.aggregate(total=Sum('subtotal'))['total'] or 0

    if checkout_data:
        id_user = current_user
        start_date_str = checkout_data['start_date']
        end_date_str = checkout_data['end_date']
        address = checkout_data['address']

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        delta = end_date - start_date
        jumlah_hari = delta.days

        grand_total = jumlah_hari * total_harga

        if request.method == "POST":

            payment_receipt_image_path = request.FILES.get('payment_receipt_image_path')

            try:
                # Buat sebuah Order baru
                order = Order.objects.create(
                    id_user=id_user,
                    start_date=start_date,
                    end_date=end_date,
                    grand_total=grand_total,
                    status="Unconfirm",
                    payment_receipt_image_path=payment_receipt_image_path,
                    address=address
                )

                for cart_item in cart_items:
                    ordered_quantity = cart_item.quantity
                    product = cart_item.id_product
                    OrderItem.objects.create(
                        id_order=order,
                        id_product=product,
                        quantity=ordered_quantity,
                        subtotal=cart_item.subtotal
                    )
                    # Kurangi stok barang setelah pembayaran berhasil
                    product.stock -= ordered_quantity
                    product.save()

                cart_items.delete()
            except Exception as e:
                print("Error:", e)
                # Tangani kesalahan dengan memberikan pesan kesalahan kepada pengguna atau kembali ke halaman checkout jika diperlukan
                messages.error(request, "An error occurred. Please try again.")
                return redirect("Order:checkoutForm")

            # Setelah pembuatan Order, tampilkan detail pembayaran pada halaman pembayaran
            return redirect("Order:pesananSaya")
        
    order_items = OrderItem.objects.filter(id_order=order)

    print(cart_items)
    context = {
        'grand_total': grand_total,
        'order': order,
        'cart_items': cart_items,
        # 'order_items': order_items,
    }
    
    return render(request, 'order/paymentOrder.html', context)


@login_required
def PesananSaya(request):
    current_user = request.user
    orders = Order.objects.filter(id_user=current_user).order_by('-create_at')
    order_details = []

    for order in orders:
        order_items = OrderItem.objects.filter(id_order=order)
        order_detail = {
            'order': order,
            'order_items': order_items
        }
        order_details.append(order_detail)

    context = {
        'order_details': order_details
    }
    return render(request, 'order/pesananSaya.html', context)
