from ..domain.ratings import Ratings
from ..infrastructure.ratingRepository import RatingRepository


class RatingService:
    def __init__(self, rating_repository: RatingRepository):
        self.rating_repository = rating_repository

    def create_rating(self, rating_data: dict) -> Ratings:
        return self.rating_repository.save(rating_data)

    def get_ratings(self) -> Ratings:
        return self.rating_repository.get()

    def get_rating_by_id(self, rating_id: int) -> Ratings:
        return self.rating_repository.get_rating_by_id(rating_id)

    def update_rating(self, rating_data: dict, rating_id: int) -> Ratings:
        return self.rating_repository.update(rating_data, rating_id)

    def delete_rating(self, rating_id: int) -> None:
        return self.rating_repository.delete(rating_id)
