from apps.users.models import User, UserRole


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_admin_by_id(user_id: int) -> User | None:
        return User.objects.filter(id=user_id, role=UserRole.ADMIN).first()
