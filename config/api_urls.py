from django.urls import include, path

urlpatterns = [
    path("user/", include("apps.tickets.urls.user_urls")),
]
