import requests
import os
import zipfile
import boto3

import logging
import logging.config
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('data-downloader')


def load_data(args):
	'''Downloads data from movielens website and uploads it to specified aws s3 bucket'''
	
	# download movielens data
	dldir = os.path.join(".","data","mdatadl.zip")
	logger.info("Downloading data") 
	r = requests.get(config.DOWNLOADURL)

	with open(dldir, 'wb') as f:  
	    f.write(r.content)

	logger.info("Download Complete. Unzipping file.")

	unzipdir = os.path.join("..","data")
	zip_ref = zipfile.ZipFile(dldir, 'r')
	zip_ref.extractall(unzipdir)
	zip_ref.close()

	moviesfile = os.path.join("..","data",config.EXTRACT_FOLDER,"movies.csv")
	ratingsfile = os.path.join("..","data",config.EXTRACT_FOLDER,"ratings.csv")

	logger.info("Uploading to S3 Bucket.")

	# Upload the files
	s3_client = boto3.client('s3')
	try:
	  response = s3_client.upload_file(moviesfile, args.bucket, 'ml-data/movies.csv')
	except Exception as e:
	  logging.error(e)

	try:
	  response = s3_client.upload_file(ratingsfile, args.bucket, 'ml-data/ratings.csv')
	except Exception as e:
	  logging.error(e)
	logger.info("S3 Upload Complete.")    
