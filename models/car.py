class Car(object):
    def __init__(self, car_id, x=0, y=0):
        self.car_id = car_id
        self.x = x
        self.y = y
        self.booked = False
        self.booked_until = None

    def distance(self, x2, y2):
        return abs(self.x - x2) + abs(self.y - y2)
