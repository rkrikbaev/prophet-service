# Saas to fit and predict with prophet and REST API

# remove --rm before production

docker run -it --rm -v ~/operator/prophet:/app -p 8000:8000 rkrikbaev/pyinstaller:prophet

#


# Build new image:

make build

# Create and Start new service

make start
