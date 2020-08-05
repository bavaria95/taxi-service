from pydantic import BaseModel


class Location(BaseModel):
    x: int
    y: int

    def distance(self, dst):
        return abs(self.x - dst.x) + abs(self.y - dst.y)


class Trip(BaseModel):
    source: Location
    destination: Location
