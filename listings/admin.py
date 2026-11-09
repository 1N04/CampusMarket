from django.contrib import admin
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'item_count')
    prepopulated_fields = {'slug': ('name',)}

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'condition', 'is_available', 'created_at')
    list_filter = ('category', 'condition', 'is_available')
    search_fields = ('title', 'description')
    list_editable = ('is_available',)
    raw_id_fields = ('seller',)
