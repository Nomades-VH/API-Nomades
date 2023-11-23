from enum import Enum


class Permissions(Enum):
    root = 9
    president = 8
    vice_president = 7
    treasurer = 6
    communicator = 5
    counselor = 4
    table = 3
    student = 2
    user = 1
    visitor = 0

# User e visitor não serão usuários do sistema

# Poderiamos criar um tipo de usuário somente para os pais dos alunos
