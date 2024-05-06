from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.db.models import Sum
from datetime import datetime

from .models import Order, OrderItem, ReturnOrder, Testimonial
from User.models import CustomUser as User
from Cart.models import Cart, CartItem


from .utils import currency

# Create your views here.
@login_required
def checkoutForm(request):
    current_user = request.user
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
            return redirect("Order:checkoutForm")

        if end_date <= start_date:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect("Order:checkoutForm")
        
        current_user = request.user
        
        request.session['checkout_data'] = {
            'id_user': current_user.id,
            'start_date': start_date,
            'end_date': end_date,
            'address': address,
        }
        return redirect("Order:paymentOrder")
        
    return render(request, 'order/formCheckout.html', { 'user_email': userEmail, 'current_user': current_user })


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
        if 'payment_receipt_image_path' in request.FILES:
            payment_receipt_image_path = request.FILES['payment_receipt_image_path']

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
                    
                    product.pricePerDay = currency(product.pricePerDay)

                cart_items.delete()
            except Exception as e:
                print("Error:", e)
                # Tangani kesalahan dengan memberikan pesan kesalahan kepada pengguna atau kembali ke halaman checkout jika diperlukan
                messages.error(request, "An error occurred. Please try again.")
                return redirect("Order:checkoutForm")

            # Setelah pembuatan Order, tampilkan detail pembayaran pada halaman pembayaran
            return redirect("Order:pesananSaya")
        else:
            messages.error(request, "Please upload the payment receipt.")
            return redirect("Order:paymentOrder")

    context = {
        'grand_total': grand_total,
        'order': order,
        'cart_items': cart_items,
        'current_user': current_user
       
    }
    
    return render(request, 'order/paymentOrder.html', context)



@login_required
def PesananSaya(request):
    current_user = request.user
    orders = Order.objects.filter(id_user=current_user).order_by('-created_at')
    order_details = []

    for order in orders:
        order_items = OrderItem.objects.filter(id_order=order)
        
        order.grand_total = currency(order.grand_total)
        for order_item in order_items:
            order_item.id_product.pricePerDay = currency(order_item.id_product.pricePerDay)
            

        
        order_detail = {
            'order': order,
            'order_items': order_items
        }
        
        order.hitung_fine()
        
        order_details.append(order_detail)

    context = {
        'current_user': current_user,
        'order_details': order_details
    }
    return render(request, 'order/pesananSaya.html', context)

@login_required
def returnOrder(request, order_id):
    order = Order.objects.get(id=order_id)
    current_user = request.user
    if request.method == 'POST':
        return_receipt_code = request.FILES.get('return_receipt_code', None)
        image = request.FILES.get('uploadFotoBarang', None)
        testimoni = request.POST.get('testimoni', None)
        photo_payment_fine = request.FILES.get('photo_payment_fine', None)
        
        # Validasi jika ada denda, gambar pembayaran denda harus diunggah
        if order.fine > 0 and not photo_payment_fine:
            messages.error(request, "Please upload the payment receipt for the fine.")
            return redirect('Order:returnOrder', order_id=order_id)

        # Jika tidak ada denda atau foto pembayaran denda sudah diunggah, proses pengembalian pesanan
        status = "Sent"  # Default status
        # Membuat objek ReturnOrder baru
        return_order = ReturnOrder.objects.create(
            id_order=order,
            return_receipt_code=return_receipt_code,
            image=image,
            photo_payment_fine=photo_payment_fine,
            status=status
        )
        
        # Jika terdapat testimoni, buat objek testimonial baru
        if testimoni:
            Testimonial.objects.create(
                id_user=current_user,
                content=testimoni
            )

        # Mengubah status pesanan menjadi "Sent"
        order.status = "Sent"
        order.save()

        return redirect('Order:pesananSaya')
    
    context = {
        'current_user': current_user,
        'order': order,
    }
    return render(request, 'order/formReturnOrder.html', context)
