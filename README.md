# How to run application:

## How to run API locally:

- (optional) create a new virtual environment (`mkvirtualenv taxi -p python3` or simply `mkvirtualenv taxi` if your default `python` is `3.8`)
- install dependencies (`pip install -r requirements.txt`)
- run the server (`uvicorn main:app --port 8080`)


## How to run API using docker

- build docker image (`docker build -t local/taxi .`)
- start container with freshly built image and expose desired port (`docker run --rm -p 8080:8080 local/taxi`)


# How to execute tests

- install development dependencies (`pip install -r requirements-dev.txt`)
- run tests with `py.test --cov=.` (also displays coverage metrics). Runs both unit and functional tests


# Swagger UI

Ones you are running application server on own local machine - your can familiarize yourself with the API structure using [Swagger docs](http://localhost:8080/docs). As with any documentation - it's not perfect, but still better than nothing!
