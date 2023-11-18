from time import sleep

from fastapi import Depends

from app.user.services import create_new_user
from ports.uow import AbstractUow

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")

    # TODO: Algumas urls ainda permitem acesso sem o token de acesso

    from bootstrap.database import ensure_all_entities

    ensure_all_entities()

    from app.uow import SqlAlchemyUow


    def _create_root(uow: AbstractUow = Depends(SqlAlchemyUow)):
        from app.user.entities import User
        from general_enum.permissions import Permissions
        from app.user.services import get_user_by_email

        root_user = get_user_by_email(uow, 'felipesampaio.contato@gmail.com')

        if not root_user:
            create_new_user(uow, User(
                username='felipe-root',
                email='felipesampaio.contato@gmail.com',
                password='FelipePy',
                permission=Permissions.root,
                fk_band=None,
            ))

    _create_root()
    import uvicorn

    uvicorn.run(app="bootstrap.server:app", host="", port=8000)
