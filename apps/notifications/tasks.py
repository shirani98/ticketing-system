import logging

from celery import shared_task

from apps.tickets.models import TicketMessage

logger = logging.getLogger(__name__)


@shared_task
def send_email_notification(message_id: int) -> None:
    message = TicketMessage.objects.select_related("ticket__order__customer").get(
        id=message_id
    )
    customer = message.ticket.order.customer
    logger.info(
        "EMAIL placeholder -> to=%s ticket=%s message=%s body=%r",
        customer.email,
        message.ticket_id,
        message.id,
        message.body[:120],
    )


@shared_task
def send_sms_notification(message_id: int) -> None:
    message = TicketMessage.objects.select_related("ticket__order__customer").get(
        id=message_id
    )
    customer = message.ticket.order.customer
    logger.info(
        "SMS placeholder -> to=%s ticket=%s message=%s body=%r",
        customer.phone or customer.username,
        message.ticket_id,
        message.id,
        message.body[:120],
    )
