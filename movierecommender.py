import logging
import logging.config
import argparse

import yaml
import pandas as pd
import pickle
from config import S3_MOVIES, S3_RATINGS
import s3fs

logging.config.fileConfig("config/logging/local.conf")


class MovieRecommender:
    def __init__(self, model_config, debug=False):

        # Set up logger and put in debug mode if debug = True
        self.logger = logging.getLogger("movierec-score")
        if debug:
            self.logger.setLevel("DEBUG")
        self.logger.debug("Logger is in debug mode")

        # Load model configuration fle
        with open(model_config, 'r') as f:
            config = yaml.load(f)

        self.logger.info("Configuration file loaded from %s", model_config)
        self.config = config

        # getting raw data from s3 bucket
        self.rawmovies = pd.read_csv(S3_MOVIES)
        self.rawratings = pd.read_csv(S3_RATINGS)

       
    def run(self, data):
        """Predicts song popularity for the input data

        Args:
            data (:py:class:`pandas.DataFrame`): DataFrame containing the data inputs for scoring

        Returns:
            results (:py:class:`numpy.Array`): Array of predictions of song popularity

        """
        print('ran')


def run_movierecommender(args):
    print('ran')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict song popularity")
    parser.add_argument("--config", "-c", default="config/test_model_config.yml",
                        help="Path to the test configuration file")
    defaultinput = 's3:/'
    parser.add_argument("--input", "-i", default="data/sample/data_to_score.csv",
                        help="Path to input data for scoring")
    parser.add_argument("--output", "-o",  default=None,
                        help="Path to where to save output predictions")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="If given, logger will be put in debug mode")
    args = parser.parse_args()

    run_movierecommender(args)