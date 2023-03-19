from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class PlanetBase(BaseModel):
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str


class PlanetCreate(BaseModel):
    name :str
    created : str
    edited : str
    url : str


class Planet(PlanetBase):
    id: int
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str


class MovieCreate(BaseModel):
    name: str
    created: str
    edited: str
    url: str
    release_date: str


class Movie(MovieBase):
    id: int
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class FavouriteCreate(BaseModel):
    # user_id: int
    planet_id: int = None
    movie_id: int = None
    title: str
