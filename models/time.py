class Time(object):
    '''
        Represents time entity in our world.
        By default we start from timestamp 0
        By calling `.tick` method we increment time in our world (by default on 1 unit)
    '''

    def __init__(self, time=0):
        self.time = time

    def __repr__(self):
        return self.time

    def tick(self, i=1):
        self.time += 1
