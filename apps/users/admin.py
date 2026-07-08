from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Ticketing", {"fields": ("phone", "role")}),
    )
    list_display = ("username", "email", "phone", "role", "is_staff")
    list_filter = ("role", "is_staff")
