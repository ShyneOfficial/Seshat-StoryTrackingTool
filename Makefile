# Makefile

PYTHON = python3
VENV = .venv
WORKDIR = app
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python

.PHONY: setup venv run api fclean request

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PY) -m spacy download en_core_web_sm

venv:
	@echo "Run this command to activate the virtual environment based on your terminal:"
	@echo "source $(VENV)/bin/activate"
	@echo "source $(VENV)/bin/activate.fish"

api:
	$(PY) -m uvicorn app.server:app --reload --port 8050

request:
	curl -s -X POST http://127.0.0.1:8050/analysis/run \
  -H "Content-Type: application/json" \
  -d @requests/analysis_test.json | python3 -m json.tool

run:
	$(PY) -m app.main

fclean:
	rm -rf $(VENV)
