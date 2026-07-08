from django.db.models import Max, Prefetch

from apps.orders.models import OrderStatus
from apps.tickets.models import Attachment, Ticket, TicketMessage


class TicketRepository:
    @staticmethod
    def _detail_queryset():
        return Ticket.objects.select_related("order", "order__customer").prefetch_related(
            Prefetch(
                "messages",
                queryset=TicketMessage.objects.prefetch_related("attachments").order_by(
                    "created_at"
                ),
            ),
            Prefetch("attachments", queryset=Attachment.objects.order_by("created_at")),
        )

    @staticmethod
    def list_for_customer(customer_id: int):
        return (
            Ticket.objects.filter(order__customer_id=customer_id)
            .select_related("order")
            .annotate(last_message_at=Max("messages__created_at"))
            .order_by("-created_at")
        )

    @staticmethod
    def get_for_customer(ticket_id: int, customer_id: int) -> Ticket | None:
        return (
            TicketRepository._detail_queryset()
            .filter(id=ticket_id, order__customer_id=customer_id)
            .first()
        )

    @staticmethod
    def get_detail_for_customer(ticket_id: int, customer_id: int) -> Ticket | None:
        return TicketRepository.get_for_customer(ticket_id, customer_id)

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
