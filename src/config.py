from os import path
import re

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
