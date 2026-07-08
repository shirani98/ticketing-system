from apps.orders.models import OrderStatus
from apps.tickets.models import Ticket


class TicketRepository:
    @staticmethod
    def list_for_customer(customer_id: int):
        return (
            Ticket.objects.filter(order__customer_id=customer_id)
            .select_related("order")
            .order_by("-created_at")
        )

    @staticmethod
    def get_for_customer(ticket_id: int, customer_id: int) -> Ticket | None:
        return (
            Ticket.objects.filter(id=ticket_id, order__customer_id=customer_id)
            .select_related("order")
            .first()
        )

    @staticmethod
    def get_by_order(order_id: int) -> Ticket | None:
        return Ticket.objects.filter(order_id=order_id).first()

    @staticmethod
    def get_by_id(ticket_id: int) -> Ticket | None:
        return (
            Ticket.objects.filter(id=ticket_id)
            .select_related("order", "order__customer")
            .first()
        )

    @staticmethod
    def list_admin_newest_first(*, delivered_only: bool = False):
        qs = Ticket.objects.select_related("order", "order__customer").order_by(
            "-created_at"
        )
        if delivered_only:
            qs = qs.filter(order__status=OrderStatus.DELIVERED)
        return qs
