from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.orders.repositories import OrderRepository
from apps.orders.serializers import OrderSerializer
from apps.users.mixins import CustomerAPIView

USER_ID_HEADER = OpenApiParameter(
    name="X-User-Id",
    type=int,
    location=OpenApiParameter.HEADER,
    required=False,
    description="Optional customer id. Defaults to the first seeded customer.",
)


class OrderListView(CustomerAPIView, ListAPIView):
    serializer_class = OrderSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self):
        return OrderRepository.list_for_customer(self.get_customer().id)

    @extend_schema(
        summary="List customer orders",
        description="Returns active and historical orders for the customer.",
        parameters=[USER_ID_HEADER],
        responses=OrderSerializer(many=True),
        auth=[],
        tags=["User"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
