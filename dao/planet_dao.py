from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from db import models
from db.models import Favourite


# --- Planets CRUD operations ---

class PlanetDao:

    def get_planets(self, db: Session,  user_id: int, skip: int = 0, limit: int = 100, q: Optional[str] = None):
        # if q:
        #     return db.query(models.Planet).filter(models.Planet.name.ilike(f"%{q}%")).offset(skip).limit(limit).all()
        # return db.query(models.Planet).offset(skip).limit(limit).all()
        if q:
            # Use custom title set by the user in Favourite table for searching planets
            if user_id:
                return db.query(models.Planet).join(Favourite, Favourite.planet_id == models.Planet.id) \
                    .filter(and_(models.Favourite.title.ilike(f"%{q}%"), Favourite.user_id == user_id)).offset(skip).limit(
                    limit).all()
            return db.query(models.Planet).filter(models.Planet.name.ilike(f"%{q}%")).offset(skip).limit(limit).all()
        return db.query(models.Planet).offset(skip).limit(limit).all()

    def get_planet_by_id(self, db: Session, planet_id: int) -> models.Planet:
        return db.query(models.Planet).filter(models.Planet.id == planet_id).first()

    def create_planet(self, db: Session, db_planet: schemas.PlanetCreate) -> models.Planet:
        # db_planet = models.Planet(**planet.dict())
        db.add(db_planet)
        db.commit()
        db.refresh(db_planet)
        return db_planet


    def delete_planet(self, db: Session, planet_id: int) -> models.Planet:
        db_planet = db.query(models.Planet).filter(models.Planet.id == planet_id).first()
        if db_planet is None:
            return None
        db.delete(db_planet)
        db.commit()
        return db_planet


planet_dao = PlanetDao()
