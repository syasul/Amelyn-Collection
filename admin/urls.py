from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('manage-product/', views.manageProduct, name='manage-product'),
    path('delete-product/<int:delete_id>/', views.deleteProduct, name='delete-product'),
    path('update-product/<int:update_id>/', views.updateProduct, name='update-product'),
    path('add-product/', views.addProduct, name='add-product'),
    path('search-product/', views.searchProduct, name='search-product')
        
]
