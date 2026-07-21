# Makefile

PYTHON = python3
VENV = .venv
WORKDIR = app
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python

.PHONY: setup venv run api clean fclean

setup: fclean
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PY) -m spacy download en_core_web_sm

venv:
	@echo "Run this command to activate the virtual environment based on your terminal:"
	@echo "source $(VENV)/bin/activate"
	@echo "source $(VENV)/bin/activate.fish"

api:
	$(PY) -m uvicorn app.server:app \
    --host 0.0.0.0 \
    --port 8050 \
    --reload

run:
	$(PY) -m app.main

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)
