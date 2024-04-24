from django.urls import path

from . import views

urlpatterns = [
    # user
    path('signup/', views.userSignUpView, name="userSignUp"),
    path('activate/<str:token>/', views.accountActivationView, name='activate'),
    path('signin/', views.userSignInView, name='userSignIn'),
    path('user/', views.userView, name='user'),

    # admin
    path('admin/', views.dashboardView, name='admin'),
    path('login-admin/', views.adminSignInView, name='adminSignIn'),
    
    # shared
    path('logout/', views.logoutView, name='logout'),
]
