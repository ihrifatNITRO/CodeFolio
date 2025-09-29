from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import random
from .forms import SignupForm
from .forms import EmailAuthenticationForm
from django.contrib import messages
from .forms import VerificationForm
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'An account with this email already exists. Please sign in instead.')
            else:
                password1 = form.cleaned_data['password1']
                code = str(random.randint(100000, 999999))
                print(f"Generated verification code for {email}: {code}")
                request.session['pending_email'] = email
                request.session['pending_password'] = password1
                request.session['verification_code'] = code
                request.session['code_created_at'] = timezone.now().isoformat()
                send_mail(
                    'Verify your CodeFolio email',
                    f'Your verification code is {code}. It expires in 10 minutes.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_email')
    else:
        form = SignupForm()
    return render(request, 'authentication/sign_up.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(
                        request, 'Please verify your email before signing in.')
                    return redirect('verify_email')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'authentication/sign_in.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            pending_email = request.session.get('pending_email')
            pending_password = request.session.get('pending_password')
            stored_code = request.session.get('verification_code')
            code_created_at = request.session.get('code_created_at')
            if pending_email and pending_password and stored_code and code_created_at:
                if code == stored_code:
                    created_time = timezone.datetime.fromisoformat(
                        code_created_at)
                    if timezone.now() > created_time + timezone.timedelta(minutes=10):
                        messages.error(
                            request, 'Verification code has expired. Please sign up again.')
                        # Clear session
                        for key in ['pending_email', 'pending_password', 'verification_code', 'code_created_at']:
                            if key in request.session:
                                del request.session[key]
                        return redirect('signup')
                    # Create user
                    user = User.objects.create_user(
                        username=pending_email,
                        email=pending_email,
                        password=pending_password
                    )
                    user.is_active = True
                    user.save()
                    login(request, user)
                    # Clear session
                    for key in ['pending_email', 'pending_password', 'verification_code', 'code_created_at']:
                        if key in request.session:
                            del request.session[key]
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid verification code.')
            else:
                messages.error(
                    request, 'Session expired. Please sign up again.')
                return redirect('signup')
        else:
            messages.error(
                request, 'Invalid code format. Please enter 6 digits.')
    else:
        form = VerificationForm()
    return render(request, 'authentication/verify.html', {'form': form})
