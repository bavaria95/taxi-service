class Time(object):
    def __init__(self, time=0):
        self.time = time

    def __repr__(self):
        return self.time

    def tick(self, i=1):
        self.time += 1
