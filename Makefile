.PHONY: test app venv clean clean-pyc clean-env clean-tests trained-model features predictions database

# Create a virtual environment named movieRec
movieRec/bin/activate: requirements.txt
	test -d movieRec || virtualenv movieRec
	. movieRec/bin/activate; pip install -r requirements.txt
	touch movieRec/bin/activate

venv: movieRec/bin/activate

# Create the database
data/msia423.db:
	python run.py create

database: data/msia423.db

# Run the Flask application
app: database
	python run.py app

all: venv app

# Run all tests
test:
	py.test

# Clean up things
clean-tests:
	rm -rf .pytest_cache
	rm -r test/model/test/
	mkdir test/model/test
	touch test/model/test/.gitkeep

clean-env:
	rm -r movieRec

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache

clean: clean-tests clean-env clean-pyc