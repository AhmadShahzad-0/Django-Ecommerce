from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get Request
        self.request = request

        #Get the current session key if it exists
        cart = self.session.get('session_key')

        #If the session does not exist, Create a new one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is available on all pages of the site
        self.cart = cart
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with the Lofin User
        if self.request.user.is_authenticated:
            # Get the Profile of the User
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # replace it '' with ""
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Update the Profile with the new Cart
            current_user.update(old_cart=carty)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with the Lofin User
        if self.request.user.is_authenticated:
            # Get the Profile of the User
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # replace it '' with ""
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Update the Profile with the new Cart
            current_user.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)
    
    def cart_totals(self):
        # Get Product IDs
        product_ids = self.cart.keys()
        # Get Products from the database
        products = Product.objects.filter(id__in=product_ids)
        # Get Quantities
        quantities = self.cart
        # Starting Counting at 0
        total = 0

        # Loop through the products and calculate the total
        for key, value in quantities.items():
            # Convert key string into Int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_on_sale:
                        total = total + (product.sale_price * value)
                    else:
                        # If not on sale, use the regular price
                        total = total + (product.price * value)

        return total

    def get_prods(self):
        #Get ids from Cart
        product_ids = self.cart.keys()
        #Get the products from the database
        products = Product.objects.filter(id__in=product_ids)
        #Return Products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get Cart
        ourcart = self.cart
        # Update Dictionary/Cart
        ourcart[product_id] = product_qty

        # Save the session
        self.session.modified = True

        # Deal with the Lofin User
        if self.request.user.is_authenticated:
            # Get the Profile of the User
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # replace it '' with ""
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Update the Profile with the new Cart
            current_user.update(old_cart=carty)

        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        # Delete the product from the cart
        if product_id in self.cart:
            del self.cart[product_id]

        # Save the session
        self.session.modified = True

        # Deal with the Lofin User
        if self.request.user.is_authenticated:
            # Get the Profile of the User
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # replace it '' with ""
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Update the Profile with the new Cart
            current_user.update(old_cart=carty)
