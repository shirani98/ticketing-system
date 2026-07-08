from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import UserRole
from apps.users.repositories import UserRepository


class CustomerAuthentication(BaseAuthentication):
    header = "HTTP_X_USER_ID"

    def authenticate(self, request):
        user_id = request.META.get(self.header)
        if not user_id:
            raise AuthenticationFailed("X-User-Id header is required.")

        try:
            user_id = int(user_id)
        except (TypeError, ValueError) as exc:
            raise AuthenticationFailed("X-User-Id must be an integer.") from exc

        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise AuthenticationFailed("User not found.")
        if user.role != UserRole.CUSTOMER:
            raise AuthenticationFailed("Customer access only.")

        return user, None
