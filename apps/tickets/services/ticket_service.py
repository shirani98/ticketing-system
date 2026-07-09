from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError

from apps.orders.models import OrderStatus
from apps.orders.repositories import OrderRepository
from apps.tickets.models import Attachment, SenderType, Ticket, TicketMessage, TicketStatus
from apps.tickets.repositories import TicketRepository
from apps.tickets.validators import validate_image_upload
from apps.notifications.services import schedule_customer_notification


class TicketService:
    REOPEN_WINDOW = timedelta(days=7)

    @classmethod
    def create_ticket(cls, customer, *, order_id, message="", description="", photo=None):
        order = OrderRepository.get_for_customer(order_id, customer.id)
        if order is None:
            raise NotFound("Order not found.")

        if TicketRepository.get_by_order(order.id):
            raise ValidationError(
                {
                    "order_id": (
                        "A ticket already exists for this order. "
                        "Re-open the existing ticket instead."
                    )
                }
            )

        body = cls._validate_creation_payload(order, message, description, photo)

        with transaction.atomic():
            ticket = Ticket.objects.create(order=order)
            ticket_message = cls._create_message(
                ticket=ticket,
                sender=customer,
                sender_type=SenderType.CUSTOMER,
                body=body,
            )
            if photo is not None:
                Attachment.objects.create(
                    ticket=ticket,
                    message=ticket_message,
                    file=photo,
                    mime_type=photo.content_type,
                    size=photo.size,
                )

        return TicketRepository.get_detail_for_customer(ticket.id, customer.id)

    @classmethod
    def add_customer_message(cls, customer, ticket_id: int, body: str):
        ticket = TicketRepository.get_for_customer(ticket_id, customer.id)
        if ticket is None:
            raise NotFound("Ticket not found.")
        if ticket.status != TicketStatus.OPEN:
            raise ValidationError({"detail": "Ticket is closed."})
        if not body.strip():
            raise ValidationError({"body": "Message is required."})

        cls._create_message(
            ticket=ticket,
            sender=customer,
            sender_type=SenderType.CUSTOMER,
            body=body.strip(),
        )
        return TicketRepository.get_detail_for_customer(ticket.id, customer.id)

    @classmethod
    def reopen_ticket(cls, customer, ticket_id: int):
        ticket = TicketRepository.get_for_customer(ticket_id, customer.id)
        if ticket is None:
            raise NotFound("Ticket not found.")
        if ticket.status != TicketStatus.CLOSED:
            raise ValidationError({"detail": "Ticket is not closed."})

        order = ticket.order
        if order.status != OrderStatus.DELIVERED:
            raise ValidationError({"detail": "Re-open is only allowed for delivered orders."})
        if order.delivered_at is None:
            raise ValidationError({"detail": "Order delivery date is missing."})

        if timezone.now() > order.delivered_at + cls.REOPEN_WINDOW:
            raise ValidationError(
                {"detail": "Re-open window has expired (1 week after delivery)."}
            )

        ticket.status = TicketStatus.OPEN
        ticket.reopened_at = timezone.now()
        ticket.save(update_fields=["status", "reopened_at", "updated_at"])
        return TicketRepository.get_detail_for_customer(ticket.id, customer.id)

    @classmethod
    def add_support_reply(cls, admin, ticket_id: int, body: str):
        ticket = TicketRepository.get_detail_admin(ticket_id)
        if ticket is None:
            raise NotFound("Ticket not found.")
        if not body.strip():
            raise ValidationError({"body": "Message is required."})

        cls._create_message(
            ticket=ticket,
            sender=admin,
            sender_type=SenderType.SUPPORT,
            body=body.strip(),
        )
        return TicketRepository.get_detail_admin(ticket.id)

    @classmethod
    def _create_message(cls, ticket, sender, sender_type, body: str) -> TicketMessage:
        message = TicketMessage.objects.create(
            ticket=ticket,
            sender=sender,
            sender_type=sender_type,
            body=body,
        )
        schedule_customer_notification(message.id)
        return message

    @staticmethod
    def _validate_creation_payload(order, message, description, photo):
        if order.status == OrderStatus.DELIVERED:
            if not description or not description.strip():
                raise ValidationError({"description": "Problem description is required."})
            if photo is None:
                raise ValidationError({"photo": "Photo upload is required."})
            validate_image_upload(photo)
            return description.strip()

        if order.status == OrderStatus.SHIPPED:
            if not message or not message.strip():
                raise ValidationError({"message": "Shipment request message is required."})
            return message.strip()

        if not message or not message.strip():
            raise ValidationError({"message": "Support message is required."})
        if photo is not None:
            raise ValidationError({"photo": "Photo upload is not allowed for this order status."})
        return message.strip()
