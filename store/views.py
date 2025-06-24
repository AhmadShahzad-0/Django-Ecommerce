from django.shortcuts import render, redirect
# store/views.py
from django.http import HttpResponse
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms



# Create your views here.
def category(request, foo):
    #Replace Hyphens with spaces in the category name
    foo = foo.replace('-', ' ')
    # Fetch products by category
    try:
        category = Category.objects.get(name=foo)  # Fetch the category by name
        products = Product.objects.filter(category=category)  # Fetch products in that category
        return render(request, 'store/category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("That Category Doesn't Exist."))
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)  # Fetch the product by primary key
    return render(request, 'store/product.html', {'product': product})  # path relative to templates/

def home(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'store/home.html', {'products':products})  # path relative to templates/

def about(request):
    return render(request, 'store/about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('home')
    else:
        return render(request, 'store/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #Login User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered successfully.")
            return redirect('home')
        
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})