from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>', views.addToCart, name='add_to_cart'),
    path('remove-product/<str:product_id>', views.removeProductFromCart, name="removeProductFromCart"),
    
    #using JS
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_product/', views.remove_product, name="remove_product")
]