from rest_framework import serializers

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "driver_name",
            "driver_phone",
            "delivered_at",
            "created_at",
        )
