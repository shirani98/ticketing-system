from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

from apps.tickets.repositories import TicketRepository
from apps.tickets.serializers import (
    CreateMessageSerializer,
    CreateTicketSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
)
from apps.tickets.services import TicketService
from apps.users.mixins import CustomerAPIView

USER_ID_HEADER = OpenApiParameter(
    name="X-User-Id",
    type=int,
    location=OpenApiParameter.HEADER,
    required=False,
    description="Optional customer id. Defaults to the first seeded customer.",
)


class TicketListCreateView(CustomerAPIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @extend_schema(
        summary="List customer tickets",
        parameters=[USER_ID_HEADER],
        responses=TicketListSerializer(many=True),
        auth=[],
        tags=["User"],
    )
    def get(self, request):
        customer = self.get_customer()
        tickets = TicketRepository.list_for_customer(customer.id)
        return Response(TicketListSerializer(tickets, many=True).data)

    @extend_schema(
        summary="Create ticket for an order",
        description=(
            "Payload depends on order status: delivered requires description + photo; "
            "shipped requires message; other statuses require message only."
        ),
        parameters=[USER_ID_HEADER],
        request={
            "multipart/form-data": CreateTicketSerializer,
            "application/json": CreateTicketSerializer,
        },
        responses={201: TicketDetailSerializer},
        auth=[],
        tags=["User"],
    )
    def post(self, request):
        customer = self.get_customer()
        serializer = CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        ticket = TicketService.create_ticket(
            customer,
            order_id=data["order_id"],
            message=data.get("message", ""),
            description=data.get("description", ""),
            photo=data.get("photo"),
        )
        return Response(TicketDetailSerializer(ticket).data, status=201)


class TicketDetailView(CustomerAPIView):
    @extend_schema(
        summary="Get ticket detail",
        parameters=[USER_ID_HEADER],
        responses={
            200: TicketDetailSerializer,
            404: OpenApiResponse(description="Ticket not found."),
        },
        auth=[],
        tags=["User"],
    )
    def get(self, request, pk):
        customer = self.get_customer()
        ticket = TicketRepository.get_detail_for_customer(pk, customer.id)
        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=404)
        return Response(TicketDetailSerializer(ticket).data)


class TicketMessageCreateView(CustomerAPIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @extend_schema(
        summary="Post message to ticket",
        parameters=[USER_ID_HEADER],
        request=CreateMessageSerializer,
        responses={201: TicketDetailSerializer},
        auth=[],
        tags=["User"],
    )
    def post(self, request, pk):
        customer = self.get_customer()
        serializer = CreateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = TicketService.add_customer_message(
            customer,
            pk,
            serializer.validated_data["body"],
        )
        return Response(TicketDetailSerializer(ticket).data, status=201)


class TicketReopenView(CustomerAPIView):
    @extend_schema(
        summary="Re-open closed ticket",
        description="Allowed only within one week of order delivery.",
        parameters=[USER_ID_HEADER],
        responses={200: TicketDetailSerializer},
        auth=[],
        tags=["User"],
    )
    def post(self, request, pk):
        customer = self.get_customer()
        ticket = TicketService.reopen_ticket(customer, pk)
        return Response(TicketDetailSerializer(ticket).data)
