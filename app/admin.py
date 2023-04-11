from django.contrib import admin
from .models import CustomUser, Cart, Product, Order
# Register your models here.

admin.site.register(CustomUser)

admin.site.register(Cart)

admin.site.register(Product)

admin.site.register(Order)

