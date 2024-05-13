from ..domain.user import User
from ..infrastructure.userRepository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict) -> User:
        return self.user_repository.save(user_data)

    def get_users(self) -> User:
        return self.user_repository.get()

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def update_user(self, user_data: dict, user_id: int) -> User:
        return self.user_repository.update(user_data, user_id)

    def delete_user(self, user_id: int) -> None:
        return self.user_repository.delete(user_id)
