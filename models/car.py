from .data import Location


class Car(object):
    def __init__(self, car_id, location=None):
        self.car_id = car_id

        if location and isinstance(location, Location):
            self.location = location
        else:
            self.location = Location(x=0, y=0)

        self.reset()

    def __repr__(self):
        return (
            f"(ID={self.car_id}, Location={self.location}, "
            f"Booked_till={self.booked_until})"
        )

    def distance(self, dst):
        return self.location.distance(dst)

    def reset(self):
        self.location = Location(x=0, y=0)
        self.booked_until = None

    def free_now(self, current_time):
        if not self.booked_until:
            return True

        if self.booked_until <= current_time:
            return True

        return False

    def book(self, src, dst, current_time, dist_to_client):
        dist_to_destination = src.distance(dst)
        trip_time = dist_to_client + dist_to_destination
        self.booked_until = current_time + trip_time
        self.location = dst

        return trip_time
