import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("movierec")

from src.dlmovdata import load_data
from src.model import create_sqlite_db, create_db
from config import BUCKET_NAME, LOC_SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_URI, DATABASE_NAME, UPLOAD_BUCKET, DOWNLOAD_BUCKET
from src.dlmovdata import download_data, load_data, load_S3toS3
from app.app import app


def run_app(args):
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('downloaddata')
    sub_process.set_defaults(func=download_data)

    sub_process = subparsers.add_parser('loadS3')
    sub_process.add_argument("--bucket", type=str, default=UPLOAD_BUCKET, help="Bucket to be copied to")
    sub_process.set_defaults(func=load_data)

    # sub_process = subparsers.add_parser('loadS3toS3')
    # sub_process.add_argument("--source", type=str, default=DOWNLOAD_BUCKET, help="Source Bucket to copy from")
    # sub_process.add_argument("--target", type=str, default=UPLOAD_BUCKET, help="Target Bucket to copy to")
    # sub_process.set_defaults(func=load_S3toS3)

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--engine_string", type=str, default=LOC_SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_db)

    sb_run = subparsers.add_parser("app", description="Run Flask app")
    sb_run.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)
