from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.orders.models import Order, OrderStatus
from apps.users.models import User, UserRole


class Command(BaseCommand):
    help = "Seed demo customers and orders for manual API testing."

    def handle(self, *args, **options):
        customer, _ = User.objects.get_or_create(
            username="customer1",
            defaults={
                "email": "customer1@example.com",
                "phone": "+10000000001",
                "role": UserRole.CUSTOMER,
            },
        )
        customer.set_password("pass")
        customer.save()

        admin, _ = User.objects.get_or_create(
            username="admin1",
            defaults={
                "email": "admin1@example.com",
                "phone": "+10000000002",
                "role": UserRole.ADMIN,
                "is_staff": True,
            },
        )
        admin.set_password("pass")
        admin.save()

        statuses = [
            OrderStatus.AWAITING_PAYMENT,
            OrderStatus.PAID,
            OrderStatus.IN_PREPARATION,
            OrderStatus.SHIPPED,
            OrderStatus.DELIVERED,
        ]

        for index, status in enumerate(statuses, start=1):
            order, created = Order.objects.get_or_create(
                customer=customer,
                status=status,
                defaults={
                    "driver_name": "Alex Driver" if status == OrderStatus.SHIPPED else "",
                    "driver_phone": "+10000000099" if status == OrderStatus.SHIPPED else "",
                    "delivered_at": timezone.now() if status == OrderStatus.DELIVERED else None,
                },
            )
            if created:
                self.stdout.write(f"Created order #{order.id} ({status})")
            else:
                self.stdout.write(f"Order already exists for status {status}")

        self.stdout.write(self.style.SUCCESS(f"Demo customer id: {customer.id}"))
        self.stdout.write(self.style.SUCCESS(f"Demo admin id: {admin.id}"))
