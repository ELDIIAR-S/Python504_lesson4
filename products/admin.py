from django.contrib import admin
from .models import Category, Product, Review

# Общие стили для всех моделей
CUSTOM_MEDIA = {
    'css': {
        'all': ('css/admin_custom.css',)
    }
}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    Media = type('Media', (), CUSTOM_MEDIA)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    Media = type('Media', (), CUSTOM_MEDIA)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'stars')
    list_filter = ('stars', 'product')
    search_fields = ('text',)
    Media = type('Media', (), CUSTOM_MEDIA)