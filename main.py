from datetime import datetime

from fastapi import FastAPI

from settings import settings
from models.time import Time
from models.car import Car
from models.taxi_park import TaxiPark
from models.data import Trip


app = FastAPI()


# the most convenient way to have shared access to some resource in our case is to
# to have them as global variables and instantiate them on application startup 
taxi_park = None
time = None


@app.on_event("startup")
def startup():
    global taxi_park
    global time

    time = Time()

    taxi_park = TaxiPark(time)
    taxi_park.populate_with_n_cars(settings.num_cars)


# healthcheck endpoint, not in the requirements, but I believe it can be useful
@app.get("/api")
async def healthcheck():
    '''
        Endpoint to be able to check that service is functioning correctly
    '''

    return {"status": "OK", "time": datetime.utcnow()}


@app.post("/api/tick")
async def tick():
    '''
        Endpoint to increase current time in the world by 1 unit
    '''

    time.tick()
    return {'time': time.time}


@app.put("/api/reset")
async def reset():
    '''
        Endpoint to reset state of the world to initial one
        i.e. moving all cars to (0, 0) point and not have any passangers
    '''

    taxi_park.reset()
    return {'status': 'OK'}


@app.post("/api/book")
async def book(trip: Trip):
    '''
        Endpoint to book a trip for a customer. Finds the closest available (== without a customer)
        car to the client location. If not car is available - we return message about failed
        car search (however request doesn't fail, it still comes with HTTP 200)
        Source and Destination points are expected inside the request body.
        Example of request body would be:
        ```
            {
              "source": {
                "x": 3,
                "y": 1
              },
              "destination": {
                "x": 8,
                "y": 6
              }
            }
        ```
    '''

    booking = taxi_park.book_closest(trip.source, trip.destination)
    if booking:
        return booking

    # here we still return HTTP code 200, even if cannot find a car
    return {"status": "failed", "message": "No free cars available right now, please wait..."}


# debug endpoint, not in the requirements, but I believe it can be useful
@app.get("/api/world")
async def world():
    '''
        Endpoint to display current state of the world, with cars' state and the current time.
    '''

    return {'cars': taxi_park.cars, 'time': time.time}
