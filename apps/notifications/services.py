from django.db import transaction

from apps.notifications.tasks import send_email_notification, send_sms_notification


def notify_customer_for_message(message_id: int) -> None:
    send_email_notification.delay(message_id)
    send_sms_notification.delay(message_id)


def schedule_customer_notification(message_id: int) -> None:
    transaction.on_commit(lambda: notify_customer_for_message(message_id))
