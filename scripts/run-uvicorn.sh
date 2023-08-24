#!/bin/sh -e

uvicorn tokenvaultapi.main:api --reload
