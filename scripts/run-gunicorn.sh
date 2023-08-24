#!/bin/sh -e

gunicorn tokenvaultapi.main:api -c tokenvaultapi/gunicorn_config.py
