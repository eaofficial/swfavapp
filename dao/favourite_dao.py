from sqlalchemy.orm import Session

from db.models import Favourite
from schemas import FavouriteCreate
from typing import List

class FavouritesDao:
    def create_favourite(self, db: Session, favourite: FavouriteCreate, user_id: int):
        db_favourite = Favourite(user_id=user_id, **favourite.dict())
        db.add(db_favourite)
        db.commit()
        db.refresh(db_favourite)
        return db_favourite

    def get_favourites_by_user_id(self, db: Session, user_id: int) -> List[Favourite]:
        return db.query(Favourite).filter(Favourite.user_id == user_id).all()

    def get_favourite_by_user_and_planet(self, db: Session, user_id: int, planet_id: int):
        return db.query(Favourite).filter(
            Favourite.user_id == user_id, Favourite.planet_id == planet_id
        ).first()


    def get_favourite_by_user_and_movie(self, db: Session, user_id: int, movie_id: int):
        return db.query(Favourite).filter(
            Favourite.user_id == user_id, Favourite.movie_id == movie_id
        ).first()


    def delete_favourite(self, db: Session, favourite_id: int):
        db.query(Favourite).filter(Favourite.id == favourite_id).delete()
        db.commit()
        return {"message": f"Favourite with ID {favourite_id} has been deleted."}


favourite_dao = FavouritesDao()