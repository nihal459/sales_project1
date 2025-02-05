from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Inventory)
admin.site.register(Checkout)
admin.site.register(OrderedProduct)
admin.site.register(AddToCart)