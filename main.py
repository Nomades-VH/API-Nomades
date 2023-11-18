from ports.uow import AbstractUow
from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv(".env")

    # TODO: Algumas urls ainda permitem acesso sem o token de acesso

    from bootstrap.database import ensure_all_entities

    ensure_all_entities()

    from app.uow import SqlAlchemyUow


    def _create_root(uow: AbstractUow):
        from app.user.entities import User
        from general_enum.permissions import Permissions
        from app.user.services import get_user_by_email

        root_user = get_user_by_email(uow, 'felipesampaio.contato@gmail.com')

        if not root_user:
            with uow:
                uow.user.add(User(
                    username='felipe-root',
                    email='felipesampaio.contato@gmail.com',
                    password='FelipePy',
                    permission=Permissions.root.value,
                    fk_band=None
                ))

    uow = SqlAlchemyUow()

    _create_root(uow)
    import uvicorn

    uvicorn.run(app="bootstrap.server:app", host="", port=8000)
