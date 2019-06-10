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
	df['movielower'] = df['movie'].str.lower()
	movies['titlelower'] = movies['title'].str.lower()
	# merging to find movieids
	df2 = df.merge(movies,left_on='movielower',right_on='titlelower',how='left')
	# removes any movies not in database
	df2 = df2.dropna()
	df2.loc[:,['movieId']] = df2.loc[:,['movieId']].astype(int)
	df2.loc[:,['rating']] = df2.loc[:,['rating']].astype(float)
	newuserid = max(ratings.userId)+1
	df2['userId'] = newuserid

	return df2[['userId','movieId','rating']]


