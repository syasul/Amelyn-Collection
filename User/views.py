from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from allauth.account.utils import send_email_confirmation


def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create a user without saving to the database
        user = User(first_name=firstName, last_name=lastName, email=email)
        user.set_password(password)
        user.is_active = False  # Deactivate the user until email is confirmed
        user.save()

        # Send email verification
        send_email_confirmation(request, user)

        # Optionally, you can log the user in immediately after registration
        login(request, user)

        return render(request, './page/user.html', {'user': user})

    return render(request, './page/register.html')

@csrf_exempt
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Otomatis login setelah aktivasi
        authenticated_user = authenticate(request, username=user.username, password=request.POST['password'])
        if authenticated_user:
            login(request, authenticated_user)

        messages.success(request, 'Your account has been activated.')
        return redirect('User:user')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('User:login')

def loginuser(request):
    return render(request, './page/loginadmin.html')

def loginadmin(request):
    return render(request, './page/loginuser.html')

@login_required
def user(request):
    return render(request, './page/user.html')

@login_required
def admin(request):
    return render(request, './page/admin.html')

@login_required
def logout(request):
    logout(request)
    return redirect('User:register')
