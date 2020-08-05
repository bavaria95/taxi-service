from typing import Dict

from pydantic import BaseModel


class Location(BaseModel):
    x: int
    y: int


class Trip(BaseModel):
    source: Location
    destination: Location
