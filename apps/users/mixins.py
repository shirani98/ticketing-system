from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.models import UserRole
from apps.users.repositories import UserRepository


class CustomerAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_customer(self):
        user_id = self.request.headers.get("X-User-Id")
        if user_id:
            try:
                user = UserRepository.get_by_id(int(user_id))
            except (TypeError, ValueError) as exc:
                raise NotFound("Invalid X-User-Id header.") from exc
        else:
            from apps.users.models import User

            user = User.objects.filter(role=UserRole.CUSTOMER).order_by("id").first()

        if user is None or user.role != UserRole.CUSTOMER:
            raise NotFound("Customer not found.")
        return user
