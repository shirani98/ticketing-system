from rest_framework import serializers

from apps.tickets.serializers import CreateMessageSerializer, TicketDetailSerializer


class AdminTicketListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.IntegerField(source="order.id")
    customer_name = serializers.SerializerMethodField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    last_message_at = serializers.DateTimeField(allow_null=True)
    unanswered_count = serializers.IntegerField()

    def get_customer_name(self, ticket):
        customer = ticket.order.customer
        full_name = customer.get_full_name().strip()
        return full_name or customer.username


class AdminTicketDetailSerializer(TicketDetailSerializer):
    customer_name = serializers.SerializerMethodField()

    def get_customer_name(self, ticket):
        customer = ticket.order.customer
        full_name = customer.get_full_name().strip()
        return full_name or customer.username


class AdminReplySerializer(CreateMessageSerializer):
    pass
