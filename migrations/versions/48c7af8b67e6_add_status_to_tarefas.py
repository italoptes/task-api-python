from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '48c7af8b67e6'
down_revision: Union[str, Sequence[str], None] = 'f512f40aace9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


status_enum = sa.Enum(
    'PENDENTE',
    'EM_ANDAMENTO',
    'CONCLUIDA',
    name='statustarefa'
)


def upgrade() -> None:
    status_enum.create(op.get_bind())

    op.add_column(
        'tarefas',
        sa.Column(
            'status',
            status_enum,
            nullable=False,
            server_default='PENDENTE'
        )
    )

    op.alter_column(
        'tarefas',
        'status',
        server_default=None
    )


def downgrade() -> None:
    op.drop_column('tarefas', 'status')
    status_enum.drop(op.get_bind())