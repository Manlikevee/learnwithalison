from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Normalize inputs
        username = request.POST.get('username', '').strip().lower()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        # 🚫 Block '@' in username
        if '@' in username:
            messages.error(request, 'Username cannot contain "@"')
            return redirect('register')

        # Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password')

        user = None

        # ✅ Check if input is email
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None
        else:
            # ✅ Treat as username
            user = authenticate(
                request,
                username=username_or_email,
                password=password
            )

        if user is not None:
            login(request, user)

            # 🔥 SUPERUSER REDIRECT
            if user.is_superuser:
                return redirect('admin_dashboard')

            # 👤 NORMAL USER REDIRECT
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid username/email or password')
            return redirect('login')

    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html',
                # subject='Password Reset Request'

            )
            messages.success(
                request,
                'If the email exists, a password reset link has been sent.'
            )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})