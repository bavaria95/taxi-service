# How to run application:

## How to run API locally:

- (optional) create a new virtual environment (`mkvirtualenv taxi -p python3`)
- install dependencies (`pip install -r requirements.txt`)
- run the server (`uvicorn api.main:app --port 8080`)
- (optional) familiarize yourself with the API using [Swagger docs](http://localhost:8080/docs). As with any documentation it's not perfect, but still better than nothing!

## How to run API using docker
- build docker image (`docker build -t local/taxi .`)
- start container with freshly built image and expose desired port (`docker run --rm -p 8080:8080 local/taxi`)
