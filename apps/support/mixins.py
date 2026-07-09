from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.models import UserRole
from apps.users.repositories import UserRepository


class AdminAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_admin(self):
        admin_id = self.request.headers.get("X-Admin-Id")
        if admin_id:
            try:
                admin = UserRepository.get_admin_by_id(int(admin_id))
            except (TypeError, ValueError) as exc:
                raise NotFound("Invalid X-Admin-Id header.") from exc
        else:
            from apps.users.models import User

            admin = User.objects.filter(role=UserRole.ADMIN).order_by("id").first()

        if admin is None:
            raise NotFound("Admin not found.")
        return admin
