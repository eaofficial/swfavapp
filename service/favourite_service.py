from fastapi import HTTPException

from dao.favourite_dao import favourite_dao
from dao.movie_dao import movie_dao
from dao.planet_dao import planet_dao


class FavouriteService:

    def get_all_planets(self, user_id, skip, limit, q, db):
        planets = planet_dao.get_planets(user_id=user_id, db=db, skip=skip, limit=limit, q=q)
        favourite_planets = set()
        if user_id:
            user_favourites = favourite_dao.get_favourites_by_user_id(db, user_id)
            favourite_planets = set([f.planet_id for f in user_favourites if f.planet_id is not None])
        planet_list = []
        for planet in planets:
            planet_dict = planet.__dict__
            planet_id = planet_dict.pop("_sa_instance_state").identity[0]
            planet_dict["id"] = planet_id
            planet_dict["is_favourite"] = True if planet_id in favourite_planets else False
            if planet_dict["is_favourite"]:
                for f in user_favourites:
                    if f.planet_id == planet_id:
                        planet_dict["name"] = f.title
                        break
            planet_list.append(planet_dict)

        return planet_list

    def get_all_movies(self, user_id, skip, limit, q, db):
        movies = movie_dao.get_movies(db=db, user_id=user_id, q=q, skip=skip, limit=limit)
        favourite_movies = set()
        if user_id:
            user_favourites = favourite_dao.get_favourites_by_user_id(db, user_id)
            favourite_movies = set([f.movie_id for f in user_favourites if f.movie_id is not None])
        movie_list = []
        for movie in movies:
            movie_dict = movie.__dict__
            movie_id = movie_dict.pop("_sa_instance_state").identity[0]
            movie_dict["id"] = movie_id
            movie_dict["is_favourite"] = True if movie_id in favourite_movies else False
            if movie_dict["is_favourite"]:
                for f in user_favourites:
                    if f.movie_id == movie_id:
                        movie_dict["title"] = f.title
                        break
            movie_list.append(movie_dict)
        return movie_list

    def add_fav_movie(self, user_id, movie, db):
        db_movie = movie_dao.get_movie_by_id(db, movie.movie_id)
        if db_movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        fav = favourite_dao.get_favourite_by_user_and_movie(db, user_id, movie.movie_id)
        if fav is not None:
            raise HTTPException(status_code=400, detail="Movie already added to favourites")
        fav = favourite_dao.create_favourite(db, movie, user_id)

    def add_fav_planet(self, user_id, planet, db):
        db_planet = planet_dao.get_planet_by_id(db, planet.planet_id)
        if db_planet is None:
            raise HTTPException(status_code=404, detail="Planet not found")

        fav = favourite_dao.get_favourite_by_user_and_planet(db, user_id, planet.planet_id)
        if fav is not None:
            raise HTTPException(status_code=400, detail="Planet already added to favourites")
        fav = favourite_dao.create_favourite(db, planet, user_id)
        return fav


favourite_service = FavouriteService()