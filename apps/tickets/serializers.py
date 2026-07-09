from rest_framework import serializers

from apps.orders.models import OrderStatus


class DriverInfoSerializer(serializers.Serializer):
    name = serializers.CharField(source="driver_name")
    phone = serializers.CharField(source="driver_phone")


class AttachmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    file = serializers.FileField()
    mime_type = serializers.CharField()
    size = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class TicketMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    body = serializers.CharField()
    sender_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    attachments = AttachmentSerializer(many=True)


class TicketListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.IntegerField(source="order.id")
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    last_message_at = serializers.DateTimeField(allow_null=True)


class TicketDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.IntegerField(source="order.id")
    order_status = serializers.CharField(source="order.status")
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    reopened_at = serializers.DateTimeField(allow_null=True)
    driver = serializers.SerializerMethodField()
    messages = TicketMessageSerializer(many=True)
    attachments = AttachmentSerializer(many=True)

    def get_driver(self, ticket):
        if ticket.order.status != OrderStatus.SHIPPED:
            return None
        if not ticket.order.driver_name and not ticket.order.driver_phone:
            return None
        return DriverInfoSerializer(ticket.order).data


class CreateTicketSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    message = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.ImageField(required=False)


class CreateMessageSerializer(serializers.Serializer):
    body = serializers.CharField()
