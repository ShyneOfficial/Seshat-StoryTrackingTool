# Makefile

PYTHON = python3
VENV = .venv
WORKDIR = app
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python

.PHONY: setup venv run fclean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PY) -m spacy download en_core_web_sm

venv:
	@echo "Run this command to activate the virtual environment based on your terminal:"
	@echo "source $(VENV)/bin/activate"
	@echo "source $(VENV)/bin/activate.fish"

run:
	$(PY) -m app.main

fclean:
	rm -rf $(VENV)
