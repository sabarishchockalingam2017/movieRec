from app import db

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('movierec-models')

Base = declarative_base()

class Ratings(Base):
        """A database model to hold ratings """
        __tablename__ = 'ratings'
        id = Column(Integer, primary_key=True)
        userid = Column(Integer, unique=False, nullable=False)
        movieid = Column(Integer,unique=False,nullable=False)
        rating = Column(Integer, unique=False, nullable=False)
        timestamp = Column(DateTime, unique=False, nullable=True)

    def __repr__(self):
        rating_repr = "<Rating(id='%s', userid=%d,movieid=%d,rating=%d,timestamp=%d)>"
        return rating_repr % (self.id, self.userid,self.movieid,self.rating,timestamp)

class Movies(Base):
	"""A database model to hold movies. """
	__tablename__ = 'movies'
	id = Column(Integer, primary_key=True)
	title = Column(String(100), unique=False, nullable=False)
	year = Column(DateTime, unique=False, nullable=True)
	genre = Column(String(200),unique=False,nullable=False)
  	  
    def __repr__(self):
        movie_repr = "<Movie(id='%s', title=%s,year=%d,genre=%s)>"
        return movie_repr % (self.id, self.title,self.year,self.genre)


def create_db(engine=None, engine_string=None):
    """Creates a database with the data models inherited from `Base` (Ratings and Movies).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
        
    create_db(engine_string=config.SQLALCHEMY_DATABASE_URI)
