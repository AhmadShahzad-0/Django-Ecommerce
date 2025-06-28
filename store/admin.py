from django.contrib import admin
from . models import Product, Category, Order, Customer,Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Profile)

# Mix Profile info and User Info in Admin
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend the User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ('username', 'email', 'first_name', 'last_name')
    inlines = [ProfileInline]

# Unregister the default User admin
admin.site.unregister(User)

# Register the custom User admin
admin.site.register(User, UserAdmin)

