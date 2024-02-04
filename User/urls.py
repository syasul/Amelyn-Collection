from django.urls import path

from . import views

urlpatterns = [
    # user
    path('signup/', views.userSignUp, name="userSignUp"),
    path('activate/<str:token>/', views.accountActivation, name='activate'),
    path('signin/', views.userSignIn, name='userSignIn'),
    path('user/', views.user, name='user'),

    # admin
    path('admin/', views.admin, name='admin'),
    path('login-admin/', views.adminSignIn, name='adminSignIn'),
    
    # shared
    path('logout/', views.logout, name='logout'),
]
