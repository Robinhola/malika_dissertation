#!/bin/sh

echo ""
echo "Creating virtual environment"
python -m venv .venv
source .venv/bin/activate

echo ""
echo "Installing dependencies"
pip install poetry
pip install black mypy
pip install dataclasses

echo ""
echo "Installation done!"
echo "How to run?"
echo "python ./malika.py && cp a.out a.csv && open a.csv"