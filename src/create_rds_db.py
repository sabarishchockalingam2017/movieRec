from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd

Base = declarative_base()  

class Ratings(Base):
	"""A database model to hold ratings """
	__tablename__ = 'ratings'
	id = Column(Integer, primary_key=True)
	userid = Column(Integer, unique=False, nullable=False)
	movieid = Column(Integer,unique=False,nullable=False)
	rating = Column(Integer, unique=False, nullable=False)
	timestamp = Column(Date, unique=False, nullable=True)
  	  
    def __repr__(self):
        rating_repr = "<Rating(id='%s', userid=%d,movieid=%d,rating=%d,timestamp=%d)>"
        return rating_repr % (self.id, self.userid,self.movieid,self.rating,timestamp)

class Movies(Base):
	"""A database model to hold movies. """
	__tablename__ = 'movies'
	id = Column(Integer, primary_key=True)
	title = Column(String(100), unique=False, nullable=False)
	year = Column(Date, unique=False, nullable=True)
	genre = Column(String(100),unique=False,nullable=False)
  	  
    def __repr__(self):
        movie_repr = "<Movie(id='%s', title=%s,year=%d,genre=%s)>"
        return movie_repr % (self.id, self.title,self.year,self.genre)

# set up sqlite connection
engine_string = 'sqlite:////tmp/movieratings.db'
