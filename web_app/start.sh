#!/bin/bash

cd /gunicorn && python setup.py install
cd /application

gunicorn -b 0.0.0.0:8005 app:api