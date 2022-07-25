#!/bin/bash

#gunicorn --log-level info --log-file=/gunicorn.log --workers 4 --name api -b 0.0.0.0:8000 --reload server.api:api
gunicorn -c gunicorn/config.py server.api:api
