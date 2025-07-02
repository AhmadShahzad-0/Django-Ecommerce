from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from .forms import ShippingForm, PaymentForm
from django.contrib import messages
from store.models import Product

# Create your views here.
def process_order(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_totals()

        payment_form = PaymentForm(request.POST)
        my_shipping = request.session.get('my_shipping')  #  CORRECTED HERE

        if not my_shipping:
            messages.error(request, "Shipping information is missing. Please fill it out again.")
            return redirect('checkout')  # or where your shipping form is

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add Order items
            # Get the Order Id
            order_id = create_order.pk

            # Get Product Info
            for product in cart_products():
                # Get Product Id
                product_id = product.id
                # Get the Product Price
                if product.is_on_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, price=price, quantity=value)
                        create_order_item.save()

            # Delete Ourt Cart After Purchase
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add Order items
            # Get the Order Id
            order_id = create_order.pk

            # Get Product Info
            for product in cart_products():
                # Get Product Id
                product_id = product.id
                # Get the Product Price
                if product.is_on_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, price=price, quantity=value)
                        create_order_item.save()

            # Delete Ourt Cart After Purchase
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

        messages.success(request, "Your order has been placed.")
        return redirect('home')
    
    messages.error(request, "You have to add products to your cart first.")
    return redirect('home')

def billing_info(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_totals()

        # Store shipping data in session
        my_shipping = {
            'shipping_full_name': request.POST.get('shipping_full_name', ''),
            'shipping_email': request.POST.get('shipping_email', ''),
            'shipping_address1': request.POST.get('shipping_address1', ''),
            'shipping_address2': request.POST.get('shipping_address2', ''),
            'shipping_city': request.POST.get('shipping_city', ''),
            'shipping_state': request.POST.get('shipping_state', ''),
            'shipping_zipcode': request.POST.get('shipping_zipcode', ''),
            'shipping_country': request.POST.get('shipping_country', ''),
        }

        request.session['my_shipping'] = my_shipping

        billing_form = PaymentForm()
        return render(request, 'payment/billing_info.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_info': my_shipping,
            'billing_form': billing_form,
        })
    
    messages.error(request, "You have to add products to your cart first.")
    return redirect('home')

def payment_success(request):
    # View to render the payment success page.
    return render(request, 'payment/payment_success.html', {})

def checkout(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_totals()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
