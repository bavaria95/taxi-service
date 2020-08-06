class Time(object):
    '''
        Represents time entity in our world.
        By default we start from timestamp 0
        By calling `.tick` method we increment time in our world (by default on 1 unit)
    '''

    def __init__(self, time=0):
        self._time = time

    def __repr__(self):
        return self._time

    def tick(self, i=1):
        self._time += i

    @property
    def time(self):
        return self._time
