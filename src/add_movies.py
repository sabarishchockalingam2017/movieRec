# from app import db
# from app.models import UserInput
import argparse
import logging.config
import yaml
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

from src.helpers.helpers import create_connection, get_session
from config import DATABASE_NAME


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()

class UserInput(Base):
        """A database model to hold user inputs """
        __tablename__ = 'userinput'
        id = Column(Integer, primary_key=True)
        movie = Column(String(100), unique=False, nullable=False)
        rating = Column(Integer, unique=False, nullable=False)

        def __repr__(self):
          rating_repr = "<UserInput(id='%s', movie=%s,rating=%d)>"
          return rating_repr % (self.id, self.movie,self.rating)


def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.UserInput`

    Args:
        args: Argparse args - should include args.movie, args.rating

    Returns: None

    """
    if args.engine_string=="false":
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
        engine = create_connection(engine_string=engine_string)
    else:
        engine = create_connection(engine_string=args.engine_string)

    Base.metadata.create_all(engine)
    session = get_session(engine=engine)

    userinput = UserInput(movie=args.movie, rating=args.rating)
    session.add(userinput)
    session.commit()
    logger.info("Database created with input added: %s rated %s", args.movie, args.rating)
    session.close()

def add_movie(args):
    """Seeds an existing database with additional movies.

    Args:
        args: Argparse args - should include args.movie, args.rating

    Returns:None

    """

    if args.engine_string=="false":
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
    else:
        engine_string = create_connection(engine_string=args.engine_string)
    
    session = get_session(engine_string=engine_string)

    userinput = UserInput(movie=args.movie, rating=args.rating)
    session.add(userinput)
    session.commit()
    logger.info("%s rated %s add to database.", args.movie, args.rating)


def _truncate_userinput(session):
    """Deletes userinput table"""

    session.execute('''DELETE FROM userinput''')
    session.commit()


if __name__ == '__main__':

    # Add parsers for both creating a database and adding movies to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--movie", default="Rush Hour", help="Name of movie")
    sb_create.add_argument("--rating", default=5, help="Rating of movie")
    sb_create.add_argument("--engine_string",default="false",help="engine string to create Database")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--movie", default="Rush Hour", help="Movie to be added")
    sb_ingest.add_argument("--rating", default=5, help="Rating of movie")
    sb_ingest.add_argument("--engine_string",default="false", help="engine string to edit db")
    sb_ingest.set_defaults(func=add_movie)

    args = parser.parse_args()
    args.func(args)