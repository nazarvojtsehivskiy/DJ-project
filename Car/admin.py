from django.contrib import admin
from .models import Brand, Car, Review, MailingSubscription, Order


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'created_at']
    list_filter = ['brand']
    search_fields = ['name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['car', 'rating', 'session_key', 'created_at']
    list_filter = ['rating', 'created_at']


@admin.register(MailingSubscription)
class MailingSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'created_at']
    search_fields = ['email', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'total_price', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    readonly_fields = ['cart_data', 'created_at', 'updated_at']

    fieldsets = (
        ('Контактна інформація', {
            'fields': ('full_name', 'phone', 'email')
        }),
        ('Доставка', {
            'fields': ('delivery_address', 'delivery_date', 'delivery_time')
        }),
        ('Оплата та статус', {
            'fields': ('payment_method', 'status', 'total_price')
        }),
        ('Деталі замовлення', {
            'fields': ('cart_data', 'notes')
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at')
        }),
    )
# Register your models here.
