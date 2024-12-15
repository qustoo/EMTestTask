"""Alter names

Revision ID: 5dbb0ea8f37a
Revises: a8dda609992b
Create Date: 2024-12-11 01:18:17.791103

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5dbb0ea8f37a"
down_revision: Union[str, None] = "a8dda609992b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "author", sa.Column("first_name", sa.String(length=100), nullable=False)
    )
    op.add_column(
        "author", sa.Column("last_name", sa.String(length=100), nullable=False)
    )
    op.add_column("author", sa.Column("birth_date", sa.Date(), nullable=False))
    op.drop_column("author", "firstname")
    op.drop_column("author", "birthdate")
    op.drop_column("author", "lastname")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "author",
        sa.Column(
            "lastname", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "author", sa.Column("birthdate", sa.DATE(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "author",
        sa.Column(
            "firstname", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("author", "birth_date")
    op.drop_column("author", "last_name")
    op.drop_column("author", "first_name")
    # ### end Alembic commands ###
