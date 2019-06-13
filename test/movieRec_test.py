import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import src.train_model as tm
import src.process_data as proda
import pandas as pd

def test_procmovies():
	testdf = pd.DataFrame([[1, 'Toy Story (1995)',
        'Adventure|Animation|Children|Comedy|Fantasy'],
       [2, 'Jumanji (1995)', 'Adventure|Children|Fantasy'],
       [3, 'Grumpier Old Men (1995)', 'Comedy|Romance'],
       [4, 'Waiting to Exhale (1995)', 'Comedy|Drama|Romance'],
       [5, 'Father of the Bride Part II (1995)', 'Comedy']])
	testdf.columns = ['movieId', 'title', 'genres']

	totest = proda.procmovies(testdf)

	expected = pd.DataFrame([[1, 'Toy Story', 'Adventure|Animation|Children|Comedy|Fantasy',
        '1995'],
       [2, 'Jumanji', 'Adventure|Children|Fantasy', '1995'],
       [3, 'Grumpier Old Men', 'Comedy|Romance', '1995'],
       [4, 'Waiting to Exhale', 'Comedy|Drama|Romance', '1995'],
       [5, 'Father of the Bride Part II', 'Comedy', '1995']])

	expected.columns = ['movieId', 'title', 'genres', 'year']

	assert totest.equals(expected)

def test_makepredictions():
	testratings = pd.DataFrame([[1,1,5],[1,2,4],[1,3,3]],columns=['userId','movieId','rating'])
	testuserinp = pd.DataFrame([[2,1,4],[2,4,5],[2,3,3]],columns=['userId','movieId','rating'])

	algo = tm.train_model(testratings,testuserinp)

	testmovies = pd.DataFrame([[1,'A','Action','2019'],[2,'B','Comedy','2018'],
                         [3,'C','Romance','2017'],[4,'D','Comedy','2016'],
                          [5,'E','Comedy','2017']], 
                         columns=['movieId', 'title', 'genres', 'year'])
	
	testpred = tm.makepredictions(algo,testmovies,testuserinp)

	expected = pd.DataFrame([['B', 'Comedy', '2018'],
       ['E', 'Comedy', '2017']], columns=['title', 'genres', 'year'])

	assert testpred.equals(expected)