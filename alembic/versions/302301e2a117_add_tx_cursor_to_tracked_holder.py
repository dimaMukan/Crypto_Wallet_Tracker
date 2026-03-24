"""add tx cursor to tracked holder

Revision ID: 302301e2a117
Revises: 9cd8f15fd150
Create Date: 2026-03-18 20:04:30.656075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '302301e2a117'
down_revision: Union[str, Sequence[str], None] = '9cd8f15fd150'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('TrackedHolder', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_tx_sync_at', sa.DateTime(timezone=True), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table('TrackedHolder', schema=None) as batch_op:
        batch_op.drop_column('last_tx_sync_at')

    # ### end Alembic commands ###
