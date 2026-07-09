from django.urls import include, path

urlpatterns = [
    path("user/", include("config.api.user_urls")),
    path("admin/", include("config.api.admin_urls")),
]
