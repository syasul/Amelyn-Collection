from django.urls import path

from . import views

urlpatterns = [
    # order
    path('checkout-form/', views.checkoutForm, name='checkoutForm'),
    path('payment-order/', views.paymentOrder, name="paymentOrder"),
    path('pesanan-saya/', views.PesananSaya, name="pesananSaya"),
    path('return-order/<int:order_id>', views.returnOrder, name="return-order"),
    
    # testimonial
    path('testimonial/<int:id>/', views.testimonial, name="testimonial")
] 