from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['category' ,'desc', 'user', 'created_at']
    list_filter = ['category', 'user']
    search_fields = ['title__icontains']

admin.site.register(Product, ProductAdmin)

admin.site.register(Category)