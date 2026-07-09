from django.urls import include, path

from apps.orders.views.user_views import OrderListView

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="user-order-list"),
    path("", include("apps.tickets.urls.user_urls")),
]
