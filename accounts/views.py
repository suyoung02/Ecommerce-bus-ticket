from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from .forms import *
import requests
# Create your views here.
def register(request):
    if request.method == 'POST':    
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request=request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('accounts/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            messages.success(
                request=request,
                message="Please confirm your email address to complete the registration"
            )
            return redirect('register')
        else:
            messages.error(request=request, message="Register failed!") 
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")
            return redirect('home')
        else:
            messages.error(request=request, message="Login failed!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'accounts/login.html', context=context)

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!")
        return render(request, 'accounts/login.html')
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('home')