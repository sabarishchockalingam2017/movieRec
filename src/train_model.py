import argparse
import logging
import pickle

import numpy as np
import pandas as pd
from surprise import SVD, KNNBaseline, Reader, Dataset
import yaml
from src.helpers import fillin_kwargs
from collections import defaultdict

logger = logging.getLogger(__name__)

def train_model(df,userinp=pd.DataFrame(),algo=SVD(),**kwargs):
	"""Trains collaborative filtering model from surprise package
	Args:
		df:dataframe of ratings(larger dataset)
		userinp: userinput that will be combined to the larger dataset
		algo: an algorithm from the surprise package
	Return:
		algo: trained model"""

	if userinp.empty==False:
		df = pd.concat([df[['userId','movieId','rating']],userinp[['userId','movieId','rating']]])

	# reader should know what scale is
	reader = Reader(rating_scale=(1,5))
	data = Dataset.load_from_df(df[['userId','movieId','rating']],reader)
	trainset = data.build_full_trainset()
	algo.fit(trainset)
	logger.info("algorithm finished training.")
	return algo

def makepredictions(algo,movies, userinp,**kwargs):
	""" Makes predictions using the given model (algo)
	Args:
		algo: an algorithm object from the surprise package
		movies: a list of movies and their ids
		userinp: a list of movies the user inputted
	Return:
		pred: list of predictions
	"""
	userid = userinp.userId[0]
	alllist = list(movies.movieId)
	# movies user hasn't seen
	newmovielist = [m for m in alllist if m not in list(userinp.movieId)]
	pred = [algo.predict(userid,m) for m in newmovielist]

	top5pred = get_top_n(pred,n=5)

	top5mov = pd.DataFrame([mid[0] for mid in top5pred[userid]])
	top5mov.columns=['movieId']
	top5mov.loc[:,['movieId']] = top5mov.loc[:,['movieId']].astype(int)
	top5mov = top5mov.merge(movies,left_on='movieId',right_on='movieId',how='left')
	logger.info('recommendations succesfully made.')
	return top5mov.loc[:,['title','genres','year']]

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