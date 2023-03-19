from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Planet(Base):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created = Column(String)
    edited = Column(String)
    url = Column(String)



class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_date = Column(String)
    created = Column(String)
    edited = Column(String)
    url = Column(String)




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)


class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    planet_id = Column(Integer, ForeignKey("planets.id"), nullable=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=True)
    title = Column(String, nullable=True)

