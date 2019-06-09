import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "movieRec"

DATABASE_NAME = 'msia423'
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
engine_string = "{}://{}:{}@{}:{}/{}". \
  format(conn_type, user, password, host, port, DATABASE_NAME)

#SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/msia423.db'
SQLALCHEMY_DATABASE_URI = engine_string

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
