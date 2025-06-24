from django.contrib import admin
from . models import Product, Category, Order, Customer

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Customer)

# Register your models here.
