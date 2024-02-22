from django.urls import path

from . import views

urlpatterns = [
    path('', views.Cart, name='cart'),
    path('add-to-cart/<int:product_id>', views.addToCart, name='add_to_cart'),
    path('remove-menu/<int:product_id>', views.removeMenuFromCart, name="removeMenuFromCart")
    
]