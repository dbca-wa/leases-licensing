#!/bin/bash

# Convenience script for local development usage only to cut down on typing,
# poetry must be installed and the virtual environment must be activated.

poetry run python manage.py $@
