from .cart import Cart

#Context processor to make the cart available on all pages
def cart(request):
    #Return a default data from our Cart
    return {'cart': Cart(request)}