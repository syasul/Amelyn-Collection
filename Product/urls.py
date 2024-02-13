from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('search-product/', views.searchProduct, name='search-product'),
    path('delete-product/<int:delete_id>/', views.deleteProduct, name='delete-product'),
    path('update-product/<int:update_id>/', views.updateProduct, name='update-product'),
    path('add-product/', views.addProduct, name='add-product'),
    path('detail-product/<int:detail_id>', views.detailProduct, name='detail-product'),
    path('list-product/', views.listProduct, name='list-product'),
    path('manage-product/', views.manageProduct, name='manage-product'),
    
]
# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)