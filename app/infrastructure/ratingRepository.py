from typing import Union
from app.infrastructure.database import SessionLocal
from ..domain.models import Ratings
from sqlalchemy.orm import Session


class RatingRepository:
    def __init__(self, db_session: Session = None):
        self.db = db_session or SessionLocal()

    def save(self, rating_data: dict) -> Ratings:
        db_rating = Ratings(**rating_data)
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating

    def update(self, rating_data: dict, rating_id: int) -> Ratings:
        rating = self.db.query(Ratings).filter(Ratings.id == rating_id).first()
        if rating:
            for var, value in rating_data.items():
                setattr(rating, var, value)
            self.db.commit()
            self.db.refresh(rating)
            return rating
        return None  # type: ignore

    def delete(self, rating_id: int) -> None:
        rating = self.db.query(Ratings).filter(Ratings.id == rating_id).first()
        if rating:
            self.db.delete(rating)
            self.db.commit()

    def get_rating_by_id(self, rating_id: int) -> Union[Ratings, None]:
        rating = self.db.query(Ratings).filter(Ratings.id == rating_id).first()
        if rating:
            return rating

        return None

    def get(self) -> Ratings:
        ratings = self.db.query(Ratings).all()

        return ratings
