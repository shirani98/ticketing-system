from apps.orders.models import Order


class OrderRepository:
    @staticmethod
    def list_for_customer(customer_id: int):
        return Order.objects.filter(customer_id=customer_id).order_by("-created_at")

    @staticmethod
    def get_for_customer(order_id: int, customer_id: int) -> Order | None:
        return Order.objects.filter(id=order_id, customer_id=customer_id).first()

    @staticmethod
    def get_by_id(order_id: int) -> Order | None:
        return Order.objects.filter(id=order_id).select_related("customer").first()
