from datetime import datetime

from fastapi import FastAPI

from models.time import Time
from models.car import Car
from models.taxi_park import TaxiPark
from models.data import Trip


app = FastAPI()


taxi_park = None
time = None


@app.on_event("startup")
def startup():
    global taxi_park
    global time

    time = Time()

    taxi_park = TaxiPark(time)

    num_cars = 3
    for i in range(1, num_cars + 1):
        car = Car(i)
        taxi_park.add_car(car)


@app.get("/api")
async def healthcheck():
    return {"status": "OK", "time": datetime.utcnow()}


@app.post("/api/tick")
async def tick():
    time.tick()
    return {'time': time}


@app.put("/api/reset")
async def reset():
    taxi_park.reset()
    return {'status': 'OK'}


@app.post("/api/book")
async def book(trip: Trip):
    print(trip.source)
    print(trip.destination)


@app.get("/api/cars")
async def f():
    print(taxi_park.find_closest(1, 2))
    return {'cars': taxi_park.cars}
