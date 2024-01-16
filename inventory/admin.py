from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'qty', 'total_stock', 'attachments')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductAttachment)

title = "Inventory Management"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = title
