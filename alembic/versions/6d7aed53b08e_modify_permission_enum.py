"""modify permission enum

Revision ID: 6d7aed53b08e
Revises: b8f3391d1c3f
Create Date: 2025-04-18 16:55:04.583782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6d7aed53b08e'
down_revision: Union[str, None] = 'b8f3391d1c3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""add professor to permissions enum"""


# Nome do tipo ENUM e tabela/coluna
enum_name = 'permissions'
tmp_enum_name = f'{enum_name}_new'
table_name = 'users'
column_name = 'permission'

# Valores antigos e novos
old_values = (
    'root',
    'president',
    'vice_president',
    'treasurer',
    'communicator',
    'counselor',
    'table',
    'student',
)

new_values = old_values + ('professor',)

def upgrade():
    # 1. Criar novo tipo ENUM com os valores atualizados
    op.execute(f"CREATE TYPE {tmp_enum_name} AS ENUM {new_values}")

    # 2. Alterar a coluna para usar o novo tipo
    op.execute(f"""
        ALTER TABLE {table_name}
        ALTER COLUMN {column_name}
        TYPE {tmp_enum_name}
        USING {column_name}::text::{tmp_enum_name}
    """)

    # 3. Remover o tipo antigo
    op.execute(f"DROP TYPE {enum_name}")

    # 4. Renomear o novo tipo para o nome original
    op.execute(f"ALTER TYPE {tmp_enum_name} RENAME TO {enum_name}")


def downgrade():
    # Reverter a operação removendo o valor 'professor'
    op.execute(f"CREATE TYPE {tmp_enum_name} AS ENUM {old_values}")

    op.execute(f"""
        ALTER TABLE {table_name}
        ALTER COLUMN {column_name}
        TYPE {tmp_enum_name}
        USING {column_name}::text::{tmp_enum_name}
    """)

    op.execute(f"DROP TYPE {enum_name}")
    op.execute(f"ALTER TYPE {tmp_enum_name} RENAME TO {enum_name}")
