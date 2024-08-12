"""All tables in alembic

Revision ID: 80c007348819
Revises: 
Create Date: 2024-08-12 09:58:08.625479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '80c007348819'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('bands',
                    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('gub', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('meaning', sa.VARCHAR(length=600), autoincrement=False, nullable=False),
                    sa.Column('theory', sa.VARCHAR(length=600), autoincrement=False, nullable=False),
                    sa.Column('breakdown', sa.VARCHAR(length=600), autoincrement=False, nullable=False),
                    sa.Column('stretching', sa.VARCHAR(length=600), autoincrement=False, nullable=False),
                    sa.Column('created_for', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('updated_for', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='bands_pkey'),
                    sa.UniqueConstraint('gub', name='bands_gub_key'),
                    sa.UniqueConstraint('name', name='bands_name_key'),
                    postgresql_ignore_search_path=False
                    )
    op.create_index('idx_gub', 'bands', ['gub'], unique=False)
    op.create_index('idx_created_updated_for', 'bands', ['created_for', 'updated_for'], unique=False)
    op.create_index('idx_created_updated_at', 'bands', ['created_at', 'updated_at'], unique=False)
    op.create_table('users',
                    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('permission',
                              postgresql.ENUM('root', 'president', 'vice_president', 'treasurer', 'communicator',
                                              'counselor', 'table', 'student', name='permissions'), autoincrement=False,
                              nullable=False),
                    sa.Column('hub', postgresql.ENUM('Areias', 'SJBarreiro', 'Piquete', 'Silveiras', name='hubs'),
                              autoincrement=False, nullable=False),
                    sa.Column('fk_band', sa.UUID(), autoincrement=False, nullable=True),
                    sa.Column('created_for', sa.UUID(), autoincrement=False, nullable=True),
                    sa.Column('updated_for', sa.UUID(), autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['fk_band'], ['bands.id'], name='users_fk_band_fkey', ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id', name='users_pkey'),
                    sa.UniqueConstraint('email', name='users_email_key')
                    )
    op.create_index('username_index', 'users', ['username'], unique=False)
    op.create_index('email_index', 'users', ['email'], unique=False)
    op.create_table('poomsaes',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_for', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('updated_for', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='poomsaes_pkey'),
    sa.UniqueConstraint('name', name='poomsaes_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('kibon_donjaks',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_for', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('updated_for', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='kibon_donjaks_pkey'),
    sa.UniqueConstraint('name', name='kibon_donjaks_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('tokens',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('access_token', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('is_invalid', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('fk_user', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['fk_user'], ['users.id'], name='tokens_fk_user_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='tokens_pkey'),
    sa.UniqueConstraint('access_token', name='tokens_access_token_key')
    )
    op.create_index('idx_fk_user', 'tokens', ['fk_user'], unique=False)
    op.create_index('idx_fk_token', 'tokens', ['access_token'], unique=False)
    op.create_index('idx_fk_is_invalid', 'tokens', ['is_invalid'], unique=False)
    op.create_table('kicks',
                    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('created_for', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('updated_for', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='kicks_pkey'),
                    sa.UniqueConstraint('name', name='kicks_name_key')
                    )
    op.create_table('exame',
    sa.Column('fk_user', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('fk_band', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('note_poomsae', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('note_kibondonjak', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('note_kick', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('note_stretching', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('note_breakdown', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('note_theory', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('exame_date_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['fk_band'], ['bands.id'], name='exame_fk_band_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['fk_user'], ['users.id'], name='exame_fk_user_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('fk_user', name='exame_pkey')
    )
    op.create_table('band_kick',
    sa.Column('band_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('kick_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['band_id'], ['bands.id'], name='band_kick_band_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['kick_id'], ['kicks.id'], name='band_kick_kick_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('band_id', 'kick_id', name='band_kick_pkey')
    )
    op.create_table('band_poomsae',
    sa.Column('band_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('poomsae_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['band_id'], ['bands.id'], name='band_poomsae_band_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['poomsae_id'], ['poomsaes.id'], name='band_poomsae_poomsae_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('band_id', 'poomsae_id', name='band_poomsae_pkey')
    )
    op.create_table('band_kibondonjak',
    sa.Column('band_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('kibondonjak_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['band_id'], ['bands.id'], name='band_kibondonjak_band_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['kibondonjak_id'], ['kibon_donjaks.id'], name='band_kibondonjak_kibondonjak_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('band_id', 'kibondonjak_id', name='band_kibondonjak_pkey')
                    )


def downgrade() -> None:
    op.drop_index('email_index', table_name='users')
    op.drop_index('username_index', table_name='users')
    op.drop_table('users')
    op.drop_index('idx_created_updated_at', table_name='bands')
    op.drop_index('idx_created_updated_for', table_name='bands')
    op.drop_index('idx_gub', table_name='bands')
    op.drop_table('bands')
    op.drop_table('band_kibondonjak')
    op.drop_table('band_poomsae')
    op.drop_table('kicks')
    op.drop_table('band_kick')
    op.drop_table('exame')
    op.drop_index('idx_fk_is_invalid', table_name='tokens')
    op.drop_index('idx_fk_token', table_name='tokens')
    op.drop_index('idx_fk_user', table_name='tokens')
    op.drop_table('tokens')
    op.drop_table('kibon_donjaks')
    op.drop_table('poomsaes')