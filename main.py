from datetime import datetime

from fastapi import FastAPI

from models.time import Time
from models.car import Car
from models.taxi_park import TaxiPark


app = FastAPI()


taxi_park = None
current_time = None


@app.on_event("startup")
def startup():
    global taxi_park
    global current_time

    current_time = Time()

    taxi_park = TaxiPark()

    num_cars = 3
    for i in range(1, num_cars + 1):
        car = Car(i)
        taxi_park.add_car(car)


@app.get("/api")
def healthcheck():
    return {"status": "OK", "time": datetime.utcnow()}


@app.post("/api/tick")
def tick():
    current_time.tick()
    return {'current_time': current_time}


@app.put("/api/reset")
def reset():
    taxi_park.reset()
    return {'status': 'OK'}


@app.get("/api/cars")
def f():
    print(taxi_park.find_closest(1, 2))
    return {'cars': taxi_park.cars}
