from enum import Enum
import sqlalchemy as sa


class Permissions(int, Enum):
    root = 9
    president = 8
    vice_president = 7
    treasurer = 6
    communicator = 5
    counselor = 4
    table = 3
    professor = 2
    student = 1
