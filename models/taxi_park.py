from .car import Car


class TaxiPark(object):
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        if not isinstance(car, Car):
            raise TypeError("Please pass instance of Car class to .add_car()")

        self.cars.append(car)

    def find_closest(self, x, y):
        # float number representation isn't accurate, so we have to introduce
        # margin epsilon
        eps = 10e-6
        min_dist = float('inf')
        closest_cars = []
        for car in self.cars:
            dist = car.distance(x, y)
            if abs(min_dist - dist) < eps:  # the same distance
                closest_cars.append(car)
            elif dist < min_dist:
                min_dist = dist  # update current minimal distance
                closest_cars = [car]  # starting list of currently known closest cars from the start

        # finding car with the smallest ID amongst the closest ones (only the same distance)
        closest_car = min(closest_cars, key=lambda car: car.car_id)

        return (closest_car, min_dist)
