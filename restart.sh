#!/usr/bin/env bash

gunicorn --workers 1 --bind unix:main.sock -m 007 wsgi:app


