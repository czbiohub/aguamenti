help:
	@echo "lint - check code style with flake8"
	@echo "test - run tests only"
	@echo "coverage - run tests and check code coverage"

test:
	py.test

coverage:
	coverage run --source aguamenti --omit="*/test*" --module py.test
	coverage report --show-missing

lint:
	flake8 --exclude docs aguamenti

conda_install:
	conda install --file conda_requirements.txt
	pip install -r requirements.txt
	pip install .

install:
	pip install -r requirements.txt
	pip install .
