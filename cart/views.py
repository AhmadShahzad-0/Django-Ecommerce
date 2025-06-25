from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_totals()
    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #test for Post
    if request.POST.get('action') == 'post':
        #Get the product id
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #Get the product
        product = get_object_or_404(Product, id=product_id)
        #Add the product to the cart
        cart.add(product=product, quantity=product_qty)

        #Get the total number of items in the cart
        cart_quantity = cart.__len__()

        #Return a JsonResponse
        #response = JsonResponse({'Product Name':product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product added to cart successfully...")
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get the product id
        product_id = str(request.POST.get('product_id'))
        #Delete the product from the cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, "Product removed from cart successfully...")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get the product id
        product_id = str(request.POST.get('product_id'))
        product_qty = str(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Product quantity updated successfully...")
        return response
        # return redirect('cart_summary')
    