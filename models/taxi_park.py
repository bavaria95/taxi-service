from .car import Car
from .time import Time
from settings import settings


class TaxiPark(object):
    '''
        Represents our collection of taxi cars in our world.
        We store a list of Car instances and a referrence to global Time object
    '''

    def __init__(self, time):
        if not isinstance(time, Time):
            raise TypeError("Please pass an instance of Time class to the class constructor")

        self.cars = []
        self.time = time

    def add_car(self, car):
        '''
            Adds a new car to our taxi park
            Params:
            - car (Car): instance of a Car which will be added to the Taxi Park
        '''

        if not isinstance(car, Car):
            raise TypeError("Please pass an instance of Car class to .add_car()")

        self.cars.append(car)

    def populate_with_n_cars(self, n=0):
        '''
            Helper function to create N cars with consecutive IDs from 1 to N (inclusive)
            and add them to the cars collection
            Params:
            - n (int): how many cars to create and add to the collections
        '''

        for i in range(1, n + 1):
            car = Car(i)
            self.add_car(car)

    def find_closest(self, src):
        '''
            Finds the closest available car to the customer.
            Works by iterating across all cars, ignoring busy ones and
            finding all cars within the minimal distance. This method is used
            since later we want the car with the smallest ID amongst those.
            And even though `.populate_with_n_cars` method will add cars in order
            of increasing IDs - it's still possible to add cars in custom order.
            So it's the most reliable way to do so. We could also sort by double
            key of (distance INCR, car_id INCR) and take the first car, but it would
            make complexity O(N logN), while here we have O(N) (which doesn't make any
            difference when having 3 cars, but could be significant difference when having
            way more cars available)
            Params:
            - src (Location): current location of the customer

            Returns:
            tuple(
                - closest_car (int): instance of Car which is the closest and has the lowest ID,
                - min_dist (int): distance between location of the customer and closest car
            ) or None (if there are no available cars at the moment)
        '''

        min_dist = float('inf')  # current known minimal distance
        closest_cars = []  # to store all cars at current known min distance
        for car in self.cars:
            # skip car if it's not available
            if not car.free_now(self.time.time):
                continue

            dist = car.distance(src) # distance between the client and current car
            if abs(min_dist - dist) < settings.eps:  # if the same distance
                closest_cars.append(car)  # add to the list of cars withing currently known min dist
            elif dist < min_dist:  # if distance we just found is smaller than currently known
                min_dist = dist  # update current minimal distance
                closest_cars = [car]  # starting list of currently known closest cars from the start

        if not closest_cars:  # if we didn't find any free cars at all
            return

        # finding car with the smallest ID amongst the closest ones (only the same distance)
        closest_car = min(closest_cars, key=lambda car: car.car_id)

        return (closest_car, min_dist)

    def book_closest(self, src, dst):
        '''
            Books the trip on the closest taxi car to the client and drives to the destination
            First we find the closest available car.
            And then booking a trip on it.
            Params:
            - src (Location): current location of the customer
            - dst (Location): desired destination of the customer

            Returns:
            - dict (
                - car_id (int): ID of the car that accepted the trip
                - total_time (int): how long the whole trip will take the customer (waiting for taxi + the ride)
            ) or None (if there are not available cars at the moment)
        '''

        closest = self.find_closest(src)
        if not closest:
            return

        (car, dist) = closest
        total_time = car.book(src, dst, current_time=self.time.time, dist_to_client=dist)

        return (car, total_time)


    def reset(self):
        '''
            Resets all cars to the default state
            i.e. to the position (0, 0) on a grid and without passangers
        '''

        [car.reset() for car in self.cars]
