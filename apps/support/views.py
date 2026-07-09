from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

from apps.support.mixins import AdminAPIView
from apps.support.serializers import (
    AdminReplySerializer,
    AdminTicketDetailSerializer,
    AdminTicketListSerializer,
)
from apps.tickets.repositories import TicketRepository
from apps.tickets.services import TicketService

ADMIN_ID_HEADER = OpenApiParameter(
    name="X-Admin-Id",
    type=int,
    location=OpenApiParameter.HEADER,
    required=False,
    description="Optional admin id. Defaults to the first seeded admin.",
)

DELIVERED_ONLY_PARAM = OpenApiParameter(
    name="delivered_only",
    type=bool,
    location=OpenApiParameter.QUERY,
    required=False,
    description="When true, return only tickets linked to delivered orders.",
)


class AdminTicketListView(AdminAPIView):
    @extend_schema(
        summary="List tickets for support portal",
        description="Default ordering is newest to oldest.",
        parameters=[ADMIN_ID_HEADER, DELIVERED_ONLY_PARAM],
        responses=AdminTicketListSerializer(many=True),
        auth=[],
        tags=["Admin"],
    )
    def get(self, request):
        delivered_only = request.query_params.get("delivered_only", "").lower() in {
            "1",
            "true",
            "yes",
        }
        tickets = TicketRepository.list_admin_newest_first(
            delivered_only=delivered_only
        )
        return Response(AdminTicketListSerializer(tickets, many=True).data)


class AdminTicketDetailView(AdminAPIView):
    @extend_schema(
        summary="Get full ticket detail",
        parameters=[ADMIN_ID_HEADER],
        responses={
            200: AdminTicketDetailSerializer,
            404: OpenApiResponse(description="Ticket not found."),
        },
        auth=[],
        tags=["Admin"],
    )
    def get(self, request, pk):
        ticket = TicketRepository.get_detail_admin(pk)
        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=404)
        return Response(AdminTicketDetailSerializer(ticket).data)


class AdminTicketReplyView(AdminAPIView):
    parser_classes = [JSONParser]

    @extend_schema(
        summary="Post support reply",
        parameters=[ADMIN_ID_HEADER],
        request=AdminReplySerializer,
        responses={201: AdminTicketDetailSerializer},
        auth=[],
        tags=["Admin"],
    )
    def post(self, request, pk):
        admin = self.get_admin()
        serializer = AdminReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = TicketService.add_support_reply(
            admin,
            pk,
            serializer.validated_data["body"],
        )
        return Response(AdminTicketDetailSerializer(ticket).data, status=201)
