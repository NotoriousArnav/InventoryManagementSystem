from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from customer_relations.models import Customer

def custom_logout(request):
    logout(request)
    # Redirect to the home page or any other desired page after logout
    return redirect('home')  # Replace 'home' with the desired redirect URL after logout

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('storefront:login')  # Change 'home' to your storefront home URL
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email_or_phone = form.cleaned_data['username_or_email_or_phone']
            password = form.cleaned_data['password']

            if '@' in username_or_email_or_phone:
                user = authenticate(request, email=username_or_email_or_phone, password=password)
            else:
                # Check if the input is a phone number
                if username_or_email_or_phone.isdigit():
                    try:
                        # Assuming Customer model has a foreign key to the User model
                        customer = Customer.objects.get(phone_number=username_or_email_or_phone)
                        user = customer.user if customer else None
                    except Customer.DoesNotExist:
                        user = None
                else:
                    # Assume it's a username
                    user = authenticate(request, username=username_or_email_or_phone, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('/')  # Replace 'home' with the desired redirect URL after login
            else:
                messages.error(request, 'Invalid login credentials.')

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})
