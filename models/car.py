from .data import Location


class Car(object):
    '''
        Represents a single Car entity. We store information about car ID,
        current location (or location in which car will be free eventually after dropping a customer)
        and timestamp at which current taxi car would be free or since when has been free.
    '''

    def __init__(self, car_id, location=None):
        self.car_id = car_id

        self.reset()

        if location and isinstance(location, Location):
            self.location = location

    def __repr__(self):
        return (
            f"(ID={self.car_id}, Location={self.location}, "
            f"Booked_till={self.booked_until})"
        )

    def distance(self, dst):
        '''
            Calculates distance between current location and dst
            Params:
            - dst (Location): other point distance to which we want to find out

            Returns:
            - dist (int): Manhatten distance between the car and dst
        '''

        return self.location.distance(dst)

    def reset(self):
        '''
            Resets the car to ~the big bang~ initial state
        '''

        self.location = Location(x=0, y=0)  # puts the car to the origin (0, 0)
        self.booked_until = None  # "frees up" the car

    def free_now(self, current_time):
        '''
            Checks whether the car is currently free by comparing current time
            and time of last/active journey end
            Params:
            - current_time (int): current time in the world

            Returns:
            is_free (bool): whether car is currently free or not
        '''

        # if booked_until is empty - it means the car is free (no yet orders)
        if not self.booked_until:
            return True

        # if current time is larger than last trip in booked_until
        # - it means the car is already free since last trip
        if self.booked_until <= current_time:
            return True

        # otherwise car hasn't finished the trip to deliver a passanger
        return False

    def book(self, src, dst, current_time, dist_to_client):
        '''
            Books a ride for the car.
            Params:
            - src (Location): source location of the customer
            - dst (Location): destination which the customer wants to reach
            - current_time (int): current time stamp in our world
            - dist_to_client (int): distance between initial location of the car
                and source location of a customer (this parameter doesn't look good here,
                but otherwise we would have to compute the same distance twice)

            Returns:
            - trip_time (int): total trip time, including taxi reaching the source location
                of the customer and then reaching client's destination
        '''

        # how far we will have to travel after picking up passanger
        dist_to_destination = src.distance(dst)
        # total trip time for the user (incl time waiting for the taxi and the ride itself)
        trip_time = dist_to_client + dist_to_destination

        # we reserve this taxi car starting from now for total trip duration
        self.booked_until = current_time + trip_time

        # and we update location to the one to which we will reach at time `booked_until`
        self.location = dst

        return trip_time
