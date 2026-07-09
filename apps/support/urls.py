from django.urls import path

from apps.support.views import (
    AdminTicketDetailView,
    AdminTicketListView,
    AdminTicketReplyView,
)

urlpatterns = [
    path("tickets/", AdminTicketListView.as_view(), name="admin-ticket-list"),
    path("tickets/<int:pk>/", AdminTicketDetailView.as_view(), name="admin-ticket-detail"),
    path(
        "tickets/<int:pk>/reply/",
        AdminTicketReplyView.as_view(),
        name="admin-ticket-reply",
    ),
]
