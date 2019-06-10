import traceback
from flask import render_template, request, redirect, url_for
import logging.config
#from app.models import UserInput
from flask import Flask
from src.add_movies import UserInput, _truncate_userinput
from flask_sqlalchemy import SQLAlchemy
import os
import sqlalchemy as sql
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
import movierecommender as mr
import src.process_data as proda
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile(os.path.join('..','config','flask_config.py'))

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("movieRecapp")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

appmr = mr.MovieRecommender()
recout=pd.DataFrame(columns=['title','genres','year'])


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        userinput = db.session.query(UserInput).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', userinput=userinput)
    except:
        traceback.print_exc()
        logger.warning("Not able to display movies, error page returned")
        return render_template('error.html')


@app.route('/submit', methods=['POST'])
def submit_entry():
    """Add movies to RDS, which will be used for predictions later. Also reset for starting over to make new predictions.

    :return: redirect to index page
    """
    # user adding input
    if request.form['submitbtn'] == "Add":
        try:
            userinput1 = UserInput(movie=request.form['movie'], rating=request.form['rating'])
            db.session.add(userinput1)
            db.session.commit()
            logger.info("Movie: %s added, rated %s", request.form['movie'], request.form['rating'])
            return redirect(url_for('index'))
        except:
            logger.warning("Not able to display movies, error page returned")
            return render_template('error.html')
    # user resetting input
    elif request.form['submitbtn'] == "Reset":
        try:
            ndel = db.session.query(UserInput).delete()
            db.session.commit()
            logger.info("removed %d rows from userinput", ndel)
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            logger.warning("Unable to delete rows, rolling back.")
            return render_template('error.html')
    # getting recommendations
    elif request.form['submitbtn'] == "GetRecommendation":
        try:
            userinp=proda.procuserinput(appmr.movies,appmr.ratings)
            recout = appmr.run(userinp)
            tables=[recout.to_html(classes='data')]
            titles=recout.columns.values
            logger.info("displaying recommendations.")
            return render_template('index.html',tables=tables,titles=titles)
        except:
            logger.warning("Not able to display recommendations, error page returned")
            return render_template('error.html')
# @app.route('/recommendations', methods=("POST", "GET"))
# def html_table():
#     if request.form['recbtn'] == "Get Recommendation":
#         try:
#             userinp=proda.procuserinput(appmr.movies,appmr.ratings)
#             df = appmr.run(userinp)
#             return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
#         except:
#             logger.warning("Not able to display movies, error page returned")
#             return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
