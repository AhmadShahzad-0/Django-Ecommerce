from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from .forms import ShippingForm, PaymentForm
from django.contrib import messages
from store.models import Product, Profile
import datetime

# Create your views here.
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the Order
        order = Order.objects.get(id=pk)
        # Get the Order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST.get('shipping_status')
            # Check status if true or not
            if status == "true":
                # get the Order
                order = Order.objects.filter(id=pk)
                # Grab the Date and Time
                now = datetime.datetime.now()
                # Update Order
                order.update(shipped=True, date_shipped=now)
            else:
                # get the Order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)

            # Redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    
    else:
        messages.error(request,"Access Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST.get('shipping_status')
            num = request.POST.get('num')
            # get the Order
            order = Order.objects.filter(id=num)
            # Grab the Date and Time
            now = datetime.datetime.now()
            # Update Order
            order.update(shipped=False)
            # Redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST.get('shipping_status')
            num = request.POST.get('num')
            # get the Order
            order = Order.objects.filter(id=num)
            # Grab the Date and Time
            now = datetime.datetime.now()
            # Update Order
            order.update(shipped=True, date_shipped=now)
            # Redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

def process_order(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_totals()

        payment_method = request.POST.get('payment_method', 'cod')  # default to COD
        billing_form = PaymentForm(request.POST)
        my_shipping = request.session.get('my_shipping')

        if not my_shipping:
            messages.error(request, "Shipping information is missing. Please fill it out again.")
            return redirect('checkout')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        phone = my_shipping['shipping_phone']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if payment_method == 'bank' and not billing_form.is_valid():
            messages.error(request, "Please enter your name for bank transfer.")
            return redirect('billing_info')

        if request.user.is_authenticated:
            user = request.user
            order = Order(
                user=user,
                full_name=full_name,
                phone=phone,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
                payment_method=payment_method
            )
        else:
            order = Order(
                full_name=full_name,
                phone=phone,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
                payment_method=payment_method
            )

        order.save()

        for product in cart_products():
            product_id = product.id
            price = product.sale_price if product.is_on_sale else product.price

            for key, value in quantities().items():
                if int(key) == product.id:
                    OrderItem.objects.create(
                        order_id=order.pk,
                        product_id=product_id,
                        user=request.user if request.user.is_authenticated else None,
                        price=price,
                        quantity=value
                    )

        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]

        if request.user.is_authenticated:
            Profile.objects.filter(user_id=request.user.id).update(old_cart="")

        messages.success(request, "Your order has been placed successfully!")
        return redirect('home')

    messages.error(request, "You have to add products to your cart first.")
    return redirect('home')

def billing_info(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_totals()

        my_shipping = {
            'shipping_full_name': request.POST.get('shipping_full_name', ''),
            'shipping_phone': request.POST.get('shipping_phone', ''),
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
        bank_account = {
            'name': 'Shop Name',
            'number': '1234567890',
            'code': 'IFSC000123',
            'bank': 'Bank of Example'
        }

        return render(request, 'payment/billing_info.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_info': my_shipping,
            'billing_form': billing_form,
            'bank_account': bank_account,
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
