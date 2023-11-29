from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.auth.entities import Auth
from ports.repository import AbstractRepository


class AbstractAuthRepository(AbstractRepository[Auth], ABC):
    def get_by_user(self, uuid: UUID) -> Optional[Auth]:
        ...


class AuthRepository(AbstractAuthRepository):

    def add(self, entity: Auth) -> None:
        self.session.add(entity)

    def get(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(Auth.id == uuid and not Auth.is_invalid).first()

    def get_by_user(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(Auth.is_invalid and Auth.fk_user == uuid).first()

    # TODO: Não é uma boa prática apagar dados do usuário do banco de dados
    # Para TODAS as tabelas, inserir um campo chamado "deleted" booleano para que quando algo for deletado
    # Ele seja alterado de False para True. Assim, na lógica ao buscar os dados, buscaremos somente aqueles que tenham
    # O campo "deleted" como False. Desse jeito não perdemos dados do banco de dados, e também conseguimos ter um
    # Dontrole dos dados "deletados"
    def remove(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(Auth.id == uuid).first().delete()

    def update(self, entity: Auth) -> None:
        self.session.query(Auth).filter(entity.id == Auth.id).first().update(entity)

    def iter(self) -> Iterator[Auth]:
        pass
