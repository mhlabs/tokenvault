#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports tokenvaultapi tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place tokenvaultapi tests scripts --exclude=__init__.py
black tokenvaultapi tests scripts
isort tokenvaultapi tests scripts
