from .car import Car


class TaxiPark(object):
    def __init__(self, time):
        self.cars = []
        self.time = time

    def add_car(self, car):
        if not isinstance(car, Car):
            raise TypeError("Please pass instance of Car class to .add_car()")

        self.cars.append(car)

    def find_closest(self, src):
        # float number representation isn't accurate, so we have to introduce
        # margin epsilon
        eps = 10e-6
        min_dist = float('inf')
        closest_cars = []
        for car in self.cars:
            if not car.free_now(self.time.time):
                continue

            dist = car.distance(src)
            if abs(min_dist - dist) < eps:  # the same distance
                closest_cars.append(car)
            elif dist < min_dist:
                min_dist = dist  # update current minimal distance
                closest_cars = [car]  # starting list of currently known closest cars from the start

        if not closest_cars:  # if we didn't find any free cars at all
            return

        # finding car with the smallest ID amongst the closest ones (only the same distance)
        closest_car = min(closest_cars, key=lambda car: car.car_id)

        return (closest_car, min_dist)

    def book_closest(self, src, dst):
        closest = self.find_closest(src)
        if not closest:
            return

        (car, dist) = closest
        total_time = car.book(src, dst, current_time=self.time.time, dist_to_client=dist)

        return {'car_id': car.car_id, 'total_time': total_time}

    def reset(self):
        [car.reset() for car in self.cars]
