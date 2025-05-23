"""Create bio info on user

Revision ID: b8f3391d1c3f
Revises: 4755177ab035
Create Date: 2025-04-12 15:41:38.779590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8f3391d1c3f'
down_revision: Union[str, None] = '4755177ab035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(), nullable=True, default=''))

    # Atualiza todos os registros existentes com o valor ''
    op.execute("UPDATE users SET bio = '' WHERE bio IS NULL")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###
