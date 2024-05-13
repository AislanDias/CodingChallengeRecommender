from typing import Union
from app.infrastructure.database import SessionLocal
from ..domain.models import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db_session: Session = None):
        self.db = db_session or SessionLocal()

    def save(self, user_data: dict) -> User:
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_data: dict, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            for var, value in user_data.items():
                setattr(user, var, value)
            self.db.commit()
            self.db.refresh(user)
            return user
        return None  # type: ignore

    def delete(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()

    def get_user_by_id(self, user_id: int) -> Union[User, None]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return user

        return None

    def get(self) -> User:
        users = self.db.query(User).all()

        return users
