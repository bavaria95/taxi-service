from datetime import datetime

from fastapi import FastAPI

from models.car import Car
from models.taxi_park import TaxiPark


app = FastAPI()


taxi_park = None


@app.on_event("startup")
def startup():
    global taxi_park
    taxi_park = TaxiPark()

    num_cars = 3
    for i in range(1, num_cars + 1):
        car = Car(i)
        taxi_park.add_car(car)


@app.get("/api")
def healthcheck():
    return {"status": "OK", "time": datetime.utcnow()}


@app.get("/api/cars")
def f():
    print(taxi_park.find_closest(1, 2))
    return {'cars': taxi_park.cars}
