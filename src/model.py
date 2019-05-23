from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, DateTime
import sqlalchemy

import logging
import logging.config
import config
import pandas as pd

import argparse
import sys
import flask
import os

from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, DATABASE_NAME

sys.path.append(os.path.abspath(os.path.join('..')))

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


def create_sqlite_db(args):
    """Creates an sqlite database with the data models inherited from `Base` .
    Args:
        args (argument from user): String defining SQLAlchemy connection URI in the form of
    Returns:
        None
    """

    engine = sqlalchemy.create_engine(args.engine_string)
    Base.metadata.create_all(engine)
    logger.info("DB file created in data folder.")

def create_db(args):
  """Creates a database with the data models inherited from `Base` (Ratings and Movies).

  Args:
      engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
          If None, `engine_string` must be provided.
      engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
          `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.
 Returns:
      None
  """
  conn_type = "mysql+pymysql"
  user = os.environ.get("MYSQL_USER")
  password = os.environ.get("MYSQL_PASSWORD")
  host = os.environ.get("MYSQL_HOST")
  port = os.environ.get("MYSQL_PORT")
  engine_string = "{}://{}:{}@{}:{}/{}". \
      format(conn_type, user, password, host, port, DATABASE_NAME)

  engine = sqlalchemy.create_engine(engine_string)
  Base.metadata.create_all(engine)
  logger.info("Tables created in AWS RDS instance.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--database", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func(args)