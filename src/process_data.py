import logging
import argparse
import yaml
import os
import sys
import subprocess
import re
import boto3
import sqlalchemy
import pandas as pd
from collections import defaultdict
import sqlalchemy as sql
sys.path.append(os.path.abspath(os.path.join('..')))
from config import SQLALCHEMY_DATABASE_URI

from src.helpers.helpers import fillin_kwargs

logger = logging.getLogger(__name__)


def procmovies(movies):
	""" Takes movies data and parses year to create year column
	Args:
		df: movies df with columns id, name (contains name and year) and genre

	Returns:
		df: movies df with year column added.
	"""
	# extracting date
	movies['year'] = movies.title.str.extract("\((\d{4})\)", expand=True)

	# removing year at end of title
	movies.title = movies.title.str[:-7] 
	return movies

def getuserinput(engine_string=SQLALCHEMY_DATABASE_URI):
	'''Gets user input from AWS RDS. Inputs are movies and ratings.'''

	query = "SELECT * FROM userinput"

	engine = sql.create_engine(engine_string)
	df = pd.read_sql(query,con=engine)
	logger.debug('userinput queried from AWS RDS.')
	return df

def procuserinput(movies,ratings,engine_string=SQLALCHEMY_DATABASE_URI):
	"""Processed user input. Format user input to be inputted into model.

	Args:
		movies: pandas dataframe of movies and their ids
		ratings: ratings dataframe with ratings and user id.

	Returns:
		df2: dataframe with new user id, movieid and rating."""

	df = getuserinput(engine_string)
	# merging to find movieids
	df2 = df.merge(movies,left_on='movie',right_on='title',how='left')
	# removes any movies not in database
	df2 = df2.dropna()
	df2.loc[:,['movieId']] = df2.loc[:,['movieId']].astype(int)
	df2.loc[:,['rating']] = df2.loc[:,['rating']].astype(float)
	newuserid = max(ratings.userId)+1
	df2['userId'] = newuserid

	return df2[['userId','movieId','rating']]


def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n