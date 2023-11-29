from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.auth.entities import Token
from ports.repository import AbstractRepository


class AbstractAuthRepository(AbstractRepository[Token], ABC):
    ...


class AuthRepository(AbstractAuthRepository):

    def add(self, entity: Token) -> None:
        self.session.add(Token)

    def get(self, id: UUID) -> Optional[Token]:
        return self.session.query(Token).filter(Token.id == id).first()

    # TODO: Não é uma boa prática apagar dados do usuário do banco de dados
    # Para TODAS as tabelas, inserir um campo chamado "deleted" booleano para que quando algo for deletado
    # Ele seja alterado de False para True. Assim, na lógica ao buscar os dados, buscaremos somente aqueles que tenham
    # O campo "deleted" como False. Desse jeito não perdemos dados do banco de dados, e também conseguimos ter um
    # Dontrole dos dados "deletados"
    def remove(self, id: UUID) -> Optional[Token]:
        return self.session.query(Token).filter(Token.id == id).first().delete()

    def update(self, entity: Token) -> None:
        self.session.query(Token).filter(entity.id == Token.id).first().update(entity)

    def iter(self) -> Iterator[Token]:
        pass