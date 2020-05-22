.PHONY: test

help:
	@echo
	@echo "======================================================================"
	@echo
	@echo "🛠  UTILS"
	@echo
	@echo "flask:      start built-in Flask dev server"
	@echo "guni:       start gunicorn app server"
	@echo "get:        hit index endpoint"
	@echo
	@echo "📊 CODE QUALITY"
	@echo
	@echo "test:       run unit tests, view basic coverage report in terminal"
	@echo "cov:        view HTML coverage report in browser"
	@echo "lint:       lint using flake8"
	@echo "fmt:        autoformat using black"
	@echo "hooks:      set Git hooks w/ pre-commit"
	@echo
	@echo "📦 DEPENDENCIES"
	@echo
	@echo "env:        show environment info"
	@echo "deps:       list prod dependencies"
	@echo
	@echo "======================================================================"
	@echo

#
# 🛠 UTILS
#

flask:
	poetry run flask run

guni:
	poetry run gunicorn -b 127.0.0.1:5001 app:app

get:
	poetry run http http://localhost:5000

#
# 📊 CODE QUALITY
#

test:
	poetry run coverage run --source='app' -m pytest -v && poetry run coverage report -m

cov:
	poetry run coverage html; open htmlcov/index.html

lint:
	poetry run flake8 *.py

fmt:
	poetry run isort *.py; poetry run black *.py

hooks:
	poetry run pre-commit install -t pre-commit; poetry run pre-commit install -t pre-push

#
# 📦 DEPENDENCIES
#

env:
	poetry env info

deps:
	poetry show --tree --no-dev
