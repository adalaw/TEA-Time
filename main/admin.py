from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'price', 'category', 'hot', 'cold', 'date_created', 'active')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'active')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'store', 'date_created', 'status')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'hotOrCold', 'qty')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)