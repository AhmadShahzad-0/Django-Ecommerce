from django.shortcuts import render, redirect
# store/views.py
from django.http import HttpResponse
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, PasswordChangeForm, UserInfoForm
from django import forms
from django.db.models import Q  # For complex queries
import json
from cart.cart import Cart  # Import the Cart class to handle cart operations


# Create your views here.
def search_products(request):
    query = request.GET.get('q').strip()
    products = []

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return render(request, 'store/search_results.html', {'products': products, 'query': query})
    
    else:
        messages.error(request, "Please enter a search term.")
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)  # Get the current user
        form = UserInfoForm(request.POST or None, instance=current_user)  # Create a form instance with the current user data
        if form.is_valid():
            form.save()

            # Display a success message
            messages.success(request, "Your Information has been updated successfully.")
            return redirect('home')
        return render(request, 'store/update_info.html', {'form': form})
    else:
        messages.error(request, "You need to be logged in to update your Information.")
        return redirect('login')
        # return render(request, 'store/update_user.html', {'form': form})


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user  # Get the current user
        # Did they fill out the form?
        if request.method == 'POST':
            form = PasswordChangeForm(current_user, request.POST)  # Create a form instance with the current user
            # Is the form valid?
            if form.is_valid():
                form.save()
                # Re-login the user to update session data
                messages.success(request, "Your password has been updated successfully.")
                login(request, current_user)  # Re-login the user to update session data
                return redirect('home')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return render(request, 'store/update_password.html', {'form': form})

        else:
            form = PasswordChangeForm(current_user)
            return render(request, 'store/update_password.html', {'form': form})

    else:
        messages.error(request, "You need to be logged in to change your password.")
        return redirect('login')
        # return render(request, 'store/update_password.html', {'form': form})                

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)  # Get the current user
        user_form = UpdateUserForm(request.POST or None, instance=current_user)  # Create a form instance with the current user data
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)  # Re-login the user to update session data
            # Display a success message
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('home')
        return render(request, 'store/update_user.html', {'user_form': user_form})
    else:
        messages.error(request, "You need to be logged in to update your profile.")
        return redirect('login')
        # return render(request, 'store/update_user.html', {'form': form})

def category_summary(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'store/category_summary.html', {'categories': categories})  # path relative to templates/

def category(request, foo):
    #Replace Hyphens with spaces in the category name
    foo = foo.replace('-', ' ')
    # Fetch products by category
    try:
        category = Category.objects.get(name=foo)  # Fetch the category by name
        products = Product.objects.filter(category=category)  # Fetch products in that category
        return render(request, 'store/category.html', {'products': products, 'category': category})
    except:
        messages.error(request, ("That Category Doesn't Exist."))
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

            # do some shopping cart logic here
            current_user = Profile.objects.get(user__id=request.user.id)  # Get the current user
            # Check if the user has an old cart
            saved_cart = current_user.old_cart
            # If the user has an old cart, load it into the session
            if saved_cart:
                # Convert the saved cart string back to a dictionary
                converted_cart = json.loads(saved_cart)
                # Initialize the cart with the saved items
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
                    
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
            messages.success(request, "Registered Successfully - Please Fill out Your Billing Information.")
            return redirect('update_info')
        
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})