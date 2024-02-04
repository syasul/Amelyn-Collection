from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from utils.generic_utils import GenericUtils
from User.models import AccountVerification, CustomUser as User
from django.contrib import messages

# user handlers
def userSignUp(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create a user without saving to the database
        isEmailExists = User.objects.filter(email=email).exists()
        if isEmailExists:
            isEmailVerified = AccountVerification.objects.filter(user__email=email).exists()
            if isEmailVerified:
                messages.error(request, 'Email already exists. Please sign in')
                return redirect('User:userSignUp')
            else:
                messages.error(request, 'Email already exists. Please check your email to activate your account.')
                return redirect('User:userSignUp')

        user = User(first_name=firstName, last_name=lastName, email=email, username=email)
        user.set_password(password)
        user.is_active = False  # Deactivate the user until email is confirmed
        user.save()

        # Issue a token for the user
        AccountVerification.objects.filter(user__email=email).delete()

        token = GenericUtils.generateRandomHex(32)
        AccountVerification.objects.create(user=user, token=token, validUntil=timezone.now() + timedelta(days=1))

        messages.success(request, 'Account created successfully. Please check your email to activate your account.')
        return redirect('User:userSignUp')

    return render(request, 'page/user/user_signup.html')

def accountActivation(request, token):
    verification = AccountVerification.objects.get(token=token)
    if verification.validUntil < timezone.now():
        messages.error(request, 'The token has expired. Please request for a new one.')
        return redirect('User:userSignup')

    user = verification.user
    user.is_active = True
    user.save()

    verification.delete()

    messages.success(request, 'Account activated successfully. You can now login.')
    return redirect('User:userSignIn')


def userSignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.authenticate(email, password)
        if user is not None:
            login(request, user)
            return redirect('User:user')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('User:userSignIn')
    return render(request, 'page/user/user_signin.html')

@login_required
def user(request):
    return render(request, 'page/user/user.html')

# admin handlers

def adminSignIn(request):
    return render(request, 'page/admin/admin_signin.html')

@login_required
def admin(request):
    return render(request, 'page/admin/admin.html')

@login_required
def logout(request):
    logout(request)
    return redirect('User:userSignIn')
