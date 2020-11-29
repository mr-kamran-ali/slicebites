from django.contrib import admin
from .models import Customer, Order, Size, Topping, OrderItem


admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(OrderItem)