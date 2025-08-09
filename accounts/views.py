from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, TwoFactorForm
from .models import CustomUser
from django.core.mail import send_mail
import uuid
import random
from django.conf import settings

def send_otp(phone, otp):
    print(f"Simulated OTP for {phone}: {otp}")
    return True

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.verification_token = str(uuid.uuid4())
            user.save()
            verification_link = request.build_absolute_uri(f"/accounts/verify/{user.verification_token}/")
            try:
                send_mail(
                    'Verify Your Email',
                    f'Click the link to verify your email: {verification_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Registration successful. Please check your email (or terminal in DEBUG mode) to verify.')
            except Exception as e:
                messages.error(request, f'Failed to send verification email: {str(e)}. Please try again.')
                return redirect('register')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = ''
        user.save()
        messages.success(request, 'Email verified! Please set up two-factor authentication.')
        return redirect('2fa_setup')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification token.')
        return redirect('login')

def two_factor_setup(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_2fa_enabled:
        return redirect('profile')
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')
            if str(otp) == str(stored_otp):
                request.user.is_2fa_enabled = True
                request.user.save()
                del request.session['otp']
                messages.success(request, 'Two-factor authentication enabled.')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid OTP.')
    else:
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        send_otp(request.user.phone_number, otp)
        form = TwoFactorForm()
    return render(request, 'accounts/2fa_setup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_verified:
                messages.error(request, 'Please verify your email first.')
                return redirect('login')
            if user.is_2fa_enabled:
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                send_otp(user.phone_number, otp)
                request.session['user_id'] = user.id
                return redirect('2fa_verify')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')

def two_factor_verify(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')
            if str(otp) == str(stored_otp):
                user_id = request.session.get('user_id')
                user = CustomUser.objects.get(id=user_id)
                login(request, user)
                del request.session['otp']
                del request.session['user_id']
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP.')
    else:
        form = TwoFactorForm()
    return render(request, 'accounts/2fa_verify.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})