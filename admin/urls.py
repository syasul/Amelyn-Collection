from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # product
    path('manage-product/', views.manageProduct, name='manage-product'),
    path('delete-product/<int:delete_id>/', views.deleteProduct, name='delete-product'),
    path('update-product/<int:update_id>/', views.updateProduct, name='update-product'),
    path('add-product/', views.addProduct, name='add-product'),
    path('search-product/', views.searchProduct, name='search-product'),
    
    # order
    path('manage-order/', views.manageOrder, name="manage-order"),
    path('manage-order/<str:sort>/', views.manageOrder, name="manage-order"),
    path('update_status/<int:id_order>', views.update_status, name="update_status"),
    path('delete_order/<int:id_order>', views.delete_order, name="delete_order"),
    
    # return order
    path('manage-return-order/', views.manageReturnOrder, name='manage-return-order'),
    path('manage-return-order/<str:sort>/', views.manageReturnOrder, name='manage-return-order'),
    path('update-return-order/<int:id_return_order>',views.updateReturnOrder, name='update-return-order'),
    path('delete-return-order/<int:id_return_order>', views.deleteReturnOrder, name='delete-return-order'),
    
    # testimonial
    path("manage-testimonial/", views.manageTestimonial, name='manage-testimonial'),
    path("manage-testimonial/<str:sort>/", views.manageTestimonial, name='manage-testimonial'),
    path("delete-testimonial/<int:id_testimonial>", views.deleteTesimonial, name='delete-testimonial')
]
