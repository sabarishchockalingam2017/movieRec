from os import path
import re
import os

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# App config
APP_NAME = "movierec"
DEBUG = True

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config','logging','local.conf')

# Download url
DOWNLOADURL =  "http://files.grouplens.org/datasets/movielens/ml-latest.zip"

EXTRACT_FOLDER = re.search("(movielens/)(.*)(.zip)",DOWNLOADURL).group(2)

UPLOAD_BUCKET = "movierecmsia423"

# Database connection config
# conn_type = "mysql+pymysql"
# user = os.environ.get("MYSQL_USER")
# password = os.environ.get("MYSQL_PASSWORD")
# host = os.environ.get("MYSQL_HOST")
# port = os.environ.get("MYSQL_PORT")

# SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/mysql-nw-schockalingam".\
# format(conn_type, user, password, host, port)

SQLALCHEMY_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 9033
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_NAME = 'msia423'
HOST = "127.0.0.1"
BUCKET_NAME = 'downloaddata'


