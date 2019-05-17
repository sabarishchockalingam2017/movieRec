import requests
import os
import zipfile

import logging
import logging.config

# download movielens data
url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

dldir = os.path.join(os.getcwd(),"mdatadl.zip")
 
r = requests.get(url)

with open(dldir, 'wb') as f:  
    f.write(r.content)

unzipdir = os.getcwd()
zip_ref = zipfile.ZipFile(dldir, 'r')
zip_ref.extractall(unzipdir)
zip_ref.close()
