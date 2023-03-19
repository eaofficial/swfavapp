from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from db import models
from db.models import Favourite


# --- Movies CRUD operations ---

class MovieDao:
    def get_movies(self, db: Session, user_id: int, skip: int = 0, limit: int = 100, q: Optional[str] = None):
        # if q:
        #     return db.query(models.Movie).filter(models.Movie.title.ilike(f"%{q}%")).offset(skip).limit(limit).all()
        # return db.query(models.Movie).offset(skip).limit(limit).all()
        if q:
            # Use custom title set by the user in Favourite table for searching planets
            if user_id:
                return db.query(models.Movie).join(Favourite, Favourite.movie_id == models.Movie.id) \
                    .filter(and_(models.Favourite.title.ilike(f"%{q}%"), Favourite.user_id == user_id)).offset(skip).limit(
                    limit).all()
            return db.query(models.Movie).filter(models.Movie.title.ilike(f"%{q}%")).offset(skip).limit(limit).all()
        return db.query(models.Movie).offset(skip).limit(limit).all()

    def get_movie_by_id(self, db: Session, movie_id: int) -> models.Movie:
        return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    def create_movie(self, db: Session, db_movie: schemas.MovieCreate) -> models.Movie:
        # db_movie = models.Movie(**movie.dict())
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie


    def delete_movie(self, db: Session, movie_id: int) -> models.Movie:
        db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
        if db_movie is None:
            return None
        db.delete(db_movie)
        db.commit()
        return db_movie


movie_dao = MovieDao()
