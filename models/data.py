from pydantic import BaseModel


class Location(BaseModel):
    '''
        Model to represent point on a 2D grid, having integer pair of (x, y) coordinates
    '''

    x: int
    y: int

    def distance(self, dst):
        '''
            Method to compute Manhatten distance between two points on a grid
        '''

        return abs(self.x - dst.x) + abs(self.y - dst.y)


class Trip(BaseModel):
    '''
        Model to represent a customer's trip. Must contain:
        - source (with Location object of current coordinates of the customer)
        - destination (with Location object of desired coordinates to travel)
    '''

    source: Location
    destination: Location
