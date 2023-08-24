#!/bin/sh -ex

./scripts/lint.sh

pytest tests --cov=tokenvaultapi --cov-report=xml --cov-report=term-missing
