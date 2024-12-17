from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType

    ordering = ['name']


class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ["name", "price", "product_type"]
    list_filter = ["product_type"]
    search_fields = ["name"]


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
