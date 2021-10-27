from django.contrib import admin
from .models import ProductCategory, Product
from basketapp.models import Basket


admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Basket)
