# from app import db
# from app.models import UserInput
import argparse
import logging.config
from sqlalchemy.orm import sessionmaker
logger = logging.getLogger(__name__)
from src.helpers.helpers import create_connection, get_session

def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.UserInput`

    Args:
        args: Argparse args - should include args.movie, args.rating

    Returns: None

    """

    db.create_all()

    userinput = UserInput(movie=args.movie, rating=args.rating)
    db.session.add(userinput)
    db.session.commit()
    logger.info("Database created with input added: %s rated %s", args.movie, args.rating)


def add_movie(args):
    """Seeds an existing database with additional movies.

    Args:
        args: Argparse args - should include args.movie, args.rating

    Returns:None

    """

    Session = sessionmaker(bind=engine)

    userinput = UserInput(movie=args.movie, rating=args.rating)
    db.session.add(userinput)
    db.session.commit()
    logger.info("%s rated %s add to database.", args.movie, args.rating)


def _truncate_userinput(session):
    """Deletes userinput table"""

    session.execute('''DELETE FROM userinput''')


if __name__ == '__main__':

    # Add parsers for both creating a database and adding movies to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--movie", default="Rush Hour", help="Name of movie")
    sb_create.add_argument("--rating", default=5, help="Rating of movie")
    sb_create.add_argument("--local",default="false",help="create rds db or local db")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--movie", default="Rush Hour", help="Movie to be added")
    sb_ingest.add_argument("--rating", default=5, help="Rating of movie")
    sb_ingest.add_argument("--local",default="false", help="create rds db or local db")
    sb_ingest.set_defaults(func=add_movie)

    args = parser.parse_args()
    args.func(args)