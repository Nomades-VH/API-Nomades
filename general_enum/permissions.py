from enum import Enum


class Permissions(Enum):
    president = 8
    vice_president = 7
    treasurer = 6
    communicator = 5
    counselor = 4
    table = 3
    student = 2
    user = 1
    visitor = 0
