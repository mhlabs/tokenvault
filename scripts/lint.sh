#!/bin/sh -ex

mypy tokenvaultapi
flake8 tokenvaultapi tests
black tokenvaultapi tests --check
#isort tokenvaultapi tests scripts --check-only
