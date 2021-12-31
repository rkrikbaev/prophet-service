# Saas to fit and predict with prophet and REST API

# remove --rm before production

docker run -it --rm -v ~/operator/prophet:/app -p 8000:8000 rkrikbaev/pyinstaller:prophet
sudo docker run --rm -v /home/user/prophet-service/prophet-as-faceplate-service:/application -it fpcloud/prophet-env-amd64:latest /bin/bash

#

# Build new image:

make build

# Create and Start new service

make start

# compile binary from python script

## nuitka

python -m nuitka --follow-import-to=pandas --follow-import-to=numpy --nofollow-import-to=setuptools fbprophet.py

## pyinstaller

pyinstaller -F fbprophet.spec
