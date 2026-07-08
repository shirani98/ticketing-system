from django.urls import path

from apps.tickets.views.user_views import (
    OrderListView,
    TicketDetailView,
    TicketListCreateView,
    TicketMessageCreateView,
    TicketReopenView,
)

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="user-order-list"),
    path("tickets/", TicketListCreateView.as_view(), name="user-ticket-list-create"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="user-ticket-detail"),
    path(
        "tickets/<int:pk>/messages/",
        TicketMessageCreateView.as_view(),
        name="user-ticket-message-create",
    ),
    path(
        "tickets/<int:pk>/reopen/",
        TicketReopenView.as_view(),
        name="user-ticket-reopen",
    ),
]
