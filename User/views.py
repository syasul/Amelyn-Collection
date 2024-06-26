from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from utils.generic_utils import GenericUtils
from User.models import AccountVerification, CustomUser as User
from django.contrib import messages
from services.email_service import EmailService

# currency format
from .utils import currency

from User.models import CustomUser
from Product.models import Product
from Order.models import Order, Testimonial

# currency format
from .utils import currency

# user handlers


def userSignUpView(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if not firstName:
            messages.warning(request, "First name cannot be empty.")
            return redirect('User:userSignUp')

        if not lastName:
            messages.warning(request, "Last name cannot be empty.")
            return redirect('User:userSignUp')

        if not email:
            messages.warning(request, "Email cannot be empty.")
            return redirect('User:userSignUp')

        if not password:
            messages.warning(request, "Password cannot be empty.")
            return redirect('User:userSignUp')

        # Create a user without saving to the database
        isEmailExists = User.objects.filter(email=email).exists()
        if isEmailExists:
            isEmailVerified = AccountVerification.objects.filter(
                user__email=email).exists()
            if isEmailVerified:
                messages.error(request, 'Email already exists. Please sign in')
                return redirect('User:userSignUp')
            else:
                messages.error(
                    request, 'Email already exists. Please check your email to activate your account.')
                return redirect('User:userSignUp')

        user = User(first_name=firstName, last_name=lastName,
                    email=email, username=email)
        user.set_password(password)
        user.is_active = False  # Deactivate the user until email is confirmed
        user.save()

        # Issue a token for the user
        AccountVerification.objects.filter(user__email=email).delete()

        token = GenericUtils.generateRandomHex(32)
        AccountVerification.objects.create(
            user=user, token=token, validUntil=timezone.now() + timedelta(days=1))

        # Email service invocation
        EmailService().send_activation_email(user, token)

        messages.success(
            request, 'Account created successfully. Please check your email to activate your account.')
        return redirect('User:userSignUp')

    return render(request, 'user/user_signup.html')


def accountActivationView(request, token):
    verification = AccountVerification.objects.get(token=token)
    if verification.validUntil < timezone.now():
        messages.error(
            request, 'The token has expired. Please request for a new one.')
        return redirect('User:userSignup')

    user = verification.user
    user.is_active = True
    user.save()

    verification.delete()

    messages.success(
        request, 'Account activated successfully. You can now login.')
    return redirect('User:userSignIn')


def userSignInView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email:
            messages.warning(request, "Email cannot be empty.")
            return redirect('User:userSignUp')

        if not password:
            messages.warning(request, "Password cannot be empty.")
            return redirect('User:userSignUp')

        user = User.authenticate(email, password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('User:userSignIn')
    return render(request, 'user/user_signin.html')


# admin handlers


def adminSignInView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # Autentikasi superuser
                print('true')
                login(request, user)
                return redirect('User:admin')
            else:
               messages.error(request, 'Invalid email or password')
       
            
    return render(request, 'admin/admin_signin.html')


@login_required
def dashboardView(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    userCount = CustomUser.objects.filter(is_superuser=False).count()
    productCount = Product.objects.count()
    orderCount = Order.objects.count()
    
    newProduct = Product.objects.all().order_by('-created_at')
    for new_product in newProduct:
        new_product.pricePerDay = currency(new_product.pricePerDay)
    
    newTestimonial = Testimonial.objects.all().order_by('-created_at')
    
    context = {
        'userCount': userCount,
        'productCount': productCount,
        'orderCount': orderCount,
        
        'products': newProduct,
        'testimonials': newTestimonial,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def logoutView(request):
    logout(request)
    return redirect('home')
