import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("movierec")

#from src.dlmovdata import load_data
from src.model import create_sqlite_db, create_db
from config import BUCKET_NAME, SQLALCHEMY_DATABASE_URI, DATABASE_NAME, UPLOAD_BUCKET
from src.dlmovdata import load_data




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('loadS3')
    sub_process.add_argument("--bucket", type=str, default=UPLOAD_BUCKET, help="Bucket to be copied to")
    sub_process.set_defaults(func=load_data)

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--engine_string", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func(args)
