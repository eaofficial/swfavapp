from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from service.favourite_service import favourite_service
from dao.user_dao import user_dao
from dao.planet_dao import planet_dao
from dao.movie_dao import movie_dao
from db.database import SessionLocal, engine
from db import models
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.on_event('startup')
async def startup_event():
    # fetch data from the API and populate the database
    db = next(get_db())
    planets_url = 'https://swapi.dev/api/planets/'
    movies_url = 'https://swapi.dev/api/films/'

    # populate planets table
    planets_data = requests.get(planets_url).json()
    for planet_data in planets_data['results']:
        planet = models.Planet(name=planet_data['name'], created=planet_data['created'], edited=planet_data['edited'], url=planet_data['url'])
        planet_dao.create_planet(db, planet)

    # populate movies table
    movies_data = requests.get(movies_url).json()
    for movie_data in movies_data['results']:
        movie = models.Movie(title=movie_data['title'], created=movie_data['created'], edited=movie_data['edited'], url=movie_data['url'], release_date=movie_data['release_date'])
        movie_dao.create_movie(db, movie)

    # user_dao.create_user(models.User(username="Eish"), db)
    db.close()


# API to get list of all planets
@app.get("/planets")
def get_planets(skip: int = 0, limit: int = 100, user_id: int = None, q: Optional[str] = None, db: Session = Depends(get_db)):
    """
    API endpoint to get a list of all planets or search planets by name/title.

    Parameters:
    - skip: int = 0 (default 0) - number of records to skip
    - limit: int = 100 (default 100) - number of records to return
    - user_id: int = None (default None) - ID of user to get favourite planets for
    - q: Optional[str] = None (default None) - search query for planet name/title

    Returns:
    - list of planet dictionaries - [{"id": int, "name": str, "description": str, "is_favourite": bool, "title": str}, ...]
    """
    try:
        planet_list = favourite_service.get_all_planets(user_id, skip, limit, q, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return planet_list


@app.get("/movies")
def get_movies(skip: int = 0, limit: int = 100, user_id: Optional[int] = None, q: Optional[str] = None, db: Session = Depends(get_db)):
    """
    API endpoint to get a list of all movies/films or search movies/films by name/title.

    Parameters:
    - skip: int = 0 (default 0) - number of records to skip
    - limit: int = 100 (default 100) - number of records to return
    - user_id: int = None (default None) - ID of user to get favourite planets for
    - q: Optional[str] = None (default None) - search query for planet name/title

    Returns:
    - list of movies/films dictionaries - [{"id": int, "released_date": str, "description": str, "is_favourite": bool, "title": str}, ...]
    """
    try:
        movie_list = favourite_service.get_all_movies(user_id, skip, limit, q, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return movie_list


@app.post("/movies/favourites")
def add_movie_to_favourites(movie: schemas.FavouriteCreate, user_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to add a movie as favourite with custom title.

    Request: schemas.FavouriteCreate

    Parameters:
    - user_id: int = None (default None) - ID of user to get favourite planets for

    Returns:
    - schemas.FavouriteCreate
    """
    try:
        resp = favourite_service.add_fav_movie(user_id, movie, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return resp


@app.post("/planets/favourites")
def add_planet_to_favourites(planet: schemas.FavouriteCreate, user_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to add a planet as favourite with custom title.

    Request: schemas.FavouriteCreate

    Parameters:
    - user_id: int = None (default None) - ID of user to get favourite planets for

    Returns:
    - schemas.FavouriteCreate
    """
    try:
        resp = favourite_service.add_fav_planet(user_id, planet, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return resp
