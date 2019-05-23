# Example project repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: Recommend movies to users which they will enjoy. Users will be a general audience ranging from occasional to regular movie watchers. Suggesting movies that suit users' interests will open users to watch more movies they haven't seen before. This will also encourage users to return for more recommendations and share the app with others.

**Mission**: Build a recommendation system which prompts users to enter movies they like (and what they would rate them) and returns similar movies they most probably will like. The recommendation system will be a user-to-user collaborative filtered system trained on the Movie Lens dataset.

**Success criteria**: 
* *Model*: The model's efficiency will be measured by AUC of the precision-recall curve for predictions from test data. Test predictions will be top 5 movies users would likely rate high. An AUC of 0.7 is considered acceptable model performance.
* *Business*: Success of the project overall will be measured by the number of regular users amassed who return at least monthly. 100,000 regular users is the threshold set for success. The ratings users give for recommendations are also a measure for success. An average of 4.0 out of 5.0 for all ratings is set as another threshold for success.

## Planning
### Theme 1: Create a pleasant user experience
#### Epic 1: User-friendly Interface
##### Story 1: Create User Input Boxes (Movie Name and their Rating). (1 pt)
##### Story 2: Match Input to Movie in Dataset. (1 pt)
##### Story 3: Autocomplete Title Input. (1 pt)
##### Story 4: Store user input in RDS. (1 pt)
#### Epic 2: Return Recommendation
##### Story 1: Returns top 5 recommendations from model. (1 pt)
##### Story 2: Add IMBD url and picture of recommended movie.
##### Story 3: Add option to rate recommendations. (4 pts)
##### Story 4: Store recommendations in RDS. (1 pt)
#### Epic 3: Deployment
##### Story 1: Deploy app via Flask (AWS). (4 pts)

### Theme 2: Meaningful Recommendations
#### Epic 1: Build Collaborative Filtered Recommender
##### Story 1: Import Data and perform EDA. (2 pt)
##### Story 2: Create Train and Test Data set. (0 pt)
##### Story 3: Build and Train Model. (2 pt)
#### Epic 2: Test Collaborative Filtered Recommender
##### Story 1: Test Model and calculate accuracy measure. (1 pt)
##### Story 2: Optimize and tune model to achieve the AUC success threshold. (4 pt)
#### Epic 3: Build Popularity Based Recommender 
##### Story 1: List most popular movies. (0 pt)
##### Story 2: Add option for user to choose genres. (1 pt)
#### Epic 4: Store necessary items online
##### Story 1: Store model and data set in S3 to be accessed by app. (2 pts)

### Theme 3: Quality Control
#### Epic 1: Logging, version control, testing, reproducibility and documentation
##### Story 1: Add logging to facilitate troubleshooting errors. (2 pt)
##### Story 2: Create unit tests and model reproducibility tests. (8 pts)
##### Story 3: Create Github repository for version control. (1 pt)
##### Story 4: Document code for future and team members' reference (8 pts)


## Backlog
1) **3.1.3**: Create Github repository for version control. (1 pt) (COMPLETED)

2) **2.1.1**: Import Data and perform EDA. (2 pt) (PLANNED)

2) **2.1.2**: Create Train and Test Data set. (0 pt) (PLANNED)

3) **2.1.3**: Build and Train Model. (2 pt) (PLANNED)

4) **2.2.1**: Test Model and calculate accuracy measure. (1 pt) (PLANNED)

5) **2.2.2**: Optimize and tune model to achieve the AUC success threshold. (4 pt)

6) **1.1.1**: Create User Input Boxes (Movie Name and their Rating). (1 pt)

7) **1.1.2**: Match Input to Movie in Dataset. (1 pt)

8) **1.2.1**: Returns top 5 recommendations from model. (1 pt)

9) **1.2.3**: Add option to rate recommendations. (4 pts)

10) **1.3.1**: Deploy app via Flask (AWS). (4 pts)
 
11) **1.1.4**: Store user input in RDS. (1 pt)

12) **1.2.4**: Store recommendations in RDS. (1 pt)

13) **2.4.1**: Store model and data set in S3 to be accessed by app. (2 pts)

14) **3.1.1**: Add logging to facilitate troubleshooting errors. (2 pt)

## Icebox
* **1.1.3**: Autocomplete Title Input (1 pt)

* **1.2.2**: Add IMBD url and picture of recommended movie. (1 pt)

* **2.3.1**: List most popular movies. (0 pt)

* **2.3.2**: Add option for user to choose genres. (1 pt)

* **3.1.2**: Create unit tests and model reproducibility tests. (8 pts)

* **3.1.4**: Document code for future and team members' reference (8 pts)




## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv movierec

source movierec/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n movierec python=3.7
conda activate movierec
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

 To create the database in an AWS RDS instance run the following command: 

`python run.py createRDS`

 The the following RDS information must be entered into a '.mysqlconfig' file in the root directory '~/'

 ```bash
 export MYSQL_USER=
 export MYSQL_PASSWORD=
 export MYSQL_HOST=
 export MYSQL_PORT=
 ```
 
 To create a local db file in the data folder run the following command:
 
 `python run.py createSqlite`

 To download data into your s3 bucket run the following command:
 
 `python run.py loadS3 --bucket=<bucketname>`
 
### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`