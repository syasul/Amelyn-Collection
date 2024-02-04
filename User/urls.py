from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.loginuser, name='login-user'),
    path('login-admin/', views.loginadmin, name='login-admin'),
    path('user/', views.user, name='user'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout, name='logout'),
]
