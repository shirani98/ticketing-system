from django.contrib import admin

from apps.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "delivered_at", "created_at")
    list_filter = ("status",)
    search_fields = ("customer__username", "customer__email", "driver_name")
