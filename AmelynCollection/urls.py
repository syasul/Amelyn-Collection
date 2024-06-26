"""AmelynCollection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import multiprocessing

from . import views


urlpatterns = [
    path('', views.userView, name='home'),
    path('ContactUs', views.contactView, name='contact'),
    path('user/', include(('User.urls', 'User'), namespace='User')),
    path('product/', include(('Product.urls', 'Product'), namespace='Product')),
    path('cart/', include(('Cart.urls', 'Cart'), namespace='Cart')),
    path('order/', include(('Order.urls', 'Order'), namespace='Order')),
    path('admin/', include(('admin.urls', 'Admin'), namespace='Admin')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)