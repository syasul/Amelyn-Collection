from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('detail-product/<int:detail_id>', views.detailProduct, name='detail-product'),
    path('list-product/', views.listProduct, name='list-product'),
    
]   