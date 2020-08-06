import pytest
import pydantic

from models.time import Time
from models.data import Location, Trip
from models.car import Car
from models.taxi_park import TaxiPark


class TestTime:
    def test_tick(self):
        current_time = Time()
        assert current_time.time == 0

        current_time.tick()

        assert current_time.time == 1

        current_time.tick(3)
        assert current_time.time == 4


class TestLocation:
    def test_one_coordinate_missing(self):
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            Location(x=4)

    def test_casting_to_int(self):
        loc = Location(x=42.4, y=73.8)
        assert loc.x == 42
        assert loc.y == 73

    def test_distance_same_point(self):
        loc1 = Location(x=42, y=73)
        loc2 = Location(x=42, y=73)

        assert loc1.distance(loc2) == 0

    def test_distance_from_origin(self):
        loc1 = Location(x=0, y=0)
        loc2 = Location(x=4, y=7)

        assert loc1.distance(loc2) == 4 + 7

    def test_distance(self):
        loc1 = Location(x=8, y=7)
        loc2 = Location(x=7, y=17)

        assert loc1.distance(loc2) == 11

    def test_distance_symetric(self):
        loc1 = Location(x=12, y=3)
        loc2 = Location(x=8, y=3)

        assert loc1.distance(loc2) == loc2.distance(loc1) == 4


class TestTrip:
    def test_wrong_constructor(self):
        with pytest.raises(pydantic.error_wrappers.ValidationError):
            Trip(source='Boston')

        with pytest.raises(pydantic.error_wrappers.ValidationError):
            Trip(source='Boston', destination='New York')

        loc1 = Location(x=4, y=2)

        with pytest.raises(pydantic.error_wrappers.ValidationError):
            Trip(source=loc1, destination='New York')

    def test_can_access_coordinates(self):
        loc1 = Location(x=4, y=2)
        loc2 = Location(x=2, y=4)

        trip = Trip(source=loc1, destination=loc2)

        assert trip.source.x == 4
        assert trip.source.y == 2

        assert trip.destination.x == 2
        assert trip.destination.y == 4


class TestCar:
    def test_default_constructor(self):
        car = Car(car_id=1)

        assert car.location == Location(x=0, y=0)
        assert not car.booked_until

    def test_giving_location(self):
        car = Car(car_id=1, location=Location(x=4, y=3))
        assert car.location == Location(x=4, y=3)

    def test_wrong_location_in_constructor(self):
        car = Car(car_id=1, location=(4, 3))

        assert car.location == Location(x=0, y=0)

    def test_distance(self):
        car = Car(car_id=1)

        loc2 = Location(x=3, y=5)
        assert car.distance(loc2) == 8

    def test_book(self):
        car = Car(car_id=1, location=Location(x=4, y=2))

        src = Location(x=6, y=3)
        dst = Location(x=8, y=7)

        dist_to_client = car.distance(src)
        assert dist_to_client == 3

        current_time = 42

        trip_time = car.book(src, dst, current_time, dist_to_client)

        assert trip_time == 3 + 6

        assert car.location == dst
        assert car.booked_until == 42 + 3 + 6

    def test_is_actually_free_now(self):
        car = Car(car_id=1)

        assert car.free_now(current_time=0)

    def test_is_actually_not_free_now(self):
        car = Car(car_id=1)

        src = Location(x=6, y=3)
        dst = Location(x=8, y=7)

        dist_to_client = car.distance(src)
        current_time = 42

        car.book(src, dst, current_time, dist_to_client)

        assert not car.free_now(45)


    def test_reset(self):
        car = Car(car_id=1, location=Location(x=5, y=3))

        src = Location(x=6, y=3)
        dst = Location(x=8, y=7)

        dist_to_client = car.distance(src)
        current_time = 42

        car.book(src, dst, current_time, dist_to_client)

        car.reset()

        assert car.location == Location(x=0, y=0)
        assert not car.booked_until


class TestTaxiPark:
    def test_try_adding_not_a_car(self):
        time = Time()
        taxi_park = TaxiPark(time)

        with pytest.raises(TypeError):
            taxi_park.add_car('car 1')

    def test_add_car_to_collection(self):
        time = Time()
        taxi_park = TaxiPark(time)

        car = Car(car_id=42)
        taxi_park.add_car(car)

        assert len(taxi_park.cars) == 1
        assert taxi_park.cars[0].car_id == 42

    def test_populating_with_n_cars(self):
        N = 3

        time = Time()
        taxi_park = TaxiPark(time)

        taxi_park.populate_with_n_cars(N)

        assert len(taxi_park.cars) == N
        for i in range(1, N + 1):
            assert taxi_park.cars[i - 1].car_id == i

    def test_find_closest(self):
        time = Time()
        taxi_park = TaxiPark(time)

        car = Car(car_id=1, location=Location(x=2, y=4))
        taxi_park.add_car(car)

        car = Car(car_id=2, location=Location(x=100, y=100))
        taxi_park.add_car(car)

        car = Car(car_id=3, location=Location(x=1, y=20))
        taxi_park.add_car(car)

        src = Location(x=99, y=99)

        (closest_car, min_dist) = taxi_park.find_closest(src)

        assert closest_car.car_id == 2
        assert min_dist == 2

    def test_find_closest_same_distance(self):
        time = Time()
        taxi_park = TaxiPark(time)

        car = Car(car_id=1, location=Location(x=3, y=3))
        taxi_park.add_car(car)

        car = Car(car_id=2, location=Location(x=5, y=5))
        taxi_park.add_car(car)

        car = Car(car_id=3, location=Location(x=6, y=4))
        taxi_park.add_car(car)

        src = Location(x=4, y=4)

        (closest_car, min_dist) = taxi_park.find_closest(src)

        assert closest_car.car_id == 1
        assert min_dist == 2

    def test_find_closest_with_busy(self):
        time = Time()
        taxi_park = TaxiPark(time)

        car = Car(car_id=1, location=Location(x=2, y=4))
        taxi_park.add_car(car)

        car = Car(car_id=2, location=Location(x=100, y=100))
        taxi_park.add_car(car)

        car = Car(car_id=3, location=Location(x=1, y=20))
        taxi_park.add_car(car)

        src = Location(x=6, y=3)
        dst = Location(x=8, y=7)

        dist_to_client = car.distance(src)
        current_time = 42

        taxi_park.cars[1].book(src, dst, current_time, dist_to_client)

        src = Location(x=99, y=99)

        (closest_car, min_dist) = taxi_park.find_closest(src)

        assert closest_car.car_id == 3
        assert min_dist == 177

    def test_find_closest_no_available(self):
        time = Time(20)
        taxi_park = TaxiPark(time)

        taxi_park.populate_with_n_cars(3)

        for car in taxi_park.cars:
            car.booked_until = 42

        src = Location(x=5, y=5)

        booking = taxi_park.find_closest(src)
        assert not booking

    def test_book_closest(self):
        time = Time()
        taxi_park = TaxiPark(time)

        car = Car(car_id=1, location=Location(x=2, y=4))
        taxi_park.add_car(car)

        car = Car(car_id=2, location=Location(x=100, y=100))
        taxi_park.add_car(car)

        car = Car(car_id=3, location=Location(x=1, y=20))
        taxi_park.add_car(car)

        src = Location(x=99, y=99)
        dst = Location(x=90, y=90)

        (car, total_time) = taxi_park.book_closest(src, dst)

        assert car.car_id == 2
        assert total_time == 2 + 18

    def test_reset(self):
        time = Time()
        taxi_park = TaxiPark(time)

        car = Car(car_id=1, location=Location(x=2, y=4))
        car.booked_until = 42
        taxi_park.add_car(car)

        car = Car(car_id=2, location=Location(x=100, y=100))
        car.booked_until = 73
        taxi_park.add_car(car)

        car = Car(car_id=3, location=Location(x=1, y=20))
        car.booked_until = 24
        taxi_park.add_car(car)

        taxi_park.reset()

        for car in taxi_park.cars:
            assert car.location == Location(x=0, y=0)
            assert not car.booked_until
