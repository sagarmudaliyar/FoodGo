from django.contrib import admin
from .models import Restaurant, FoodItem


class FoodItemInline(admin.TabularInline):
    """
    Allows adding and editing FoodItems directly inside the Restaurant admin page.
    """
    model = FoodItem
    extra = 1
    fields = ('name', 'category', 'price', 'is_available')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for Restaurant model.
    Allows administrators to view, add, edit, and filter restaurants in PostgreSQL.
    """
    list_display = (
        'name',
        'cuisine',
        'category',
        'rating',
        'delivery_time',
        'price_for_two',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'is_active', 'rating')
    search_fields = ('name', 'cuisine', 'description')
    list_editable = ('is_active', 'rating')
    ordering = ('-rating', '-created_at')
    inlines = [FoodItemInline]


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for FoodItem model.
    Allows administrators to view, add, edit, and filter food items.
    """
    list_display = (
        'name',
        'restaurant',
        'category',
        'price',
        'is_available',
        'created_at',
    )
    search_fields = (
        'name',
        'restaurant__name',
        'category',
        'description',
    )
    list_filter = (
        'is_available',
        'category',
        'restaurant',
    )
    ordering = ('restaurant', 'name')
    list_editable = ('price', 'is_available')
