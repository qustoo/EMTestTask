"""Create models...

Revision ID: d1226d97dfc3
Revises: 
Create Date: 2024-12-10 20:52:29.748372

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1226d97dfc3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "author",
        sa.Column("firstname", sa.String(length=100), nullable=False),
        sa.Column("lastname", sa.String(length=100), nullable=False),
        sa.Column("birthdate", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_author")),
        sa.UniqueConstraint("id", name=op.f("uq_author_id")),
    )
    op.create_table(
        "book",
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.CheckConstraint("count >= 0", name=op.f("ck_book_check_count_non_negative")),
        sa.ForeignKeyConstraint(
            ["author_id"], ["author.id"], name=op.f("fk_book_author_id_author")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_book")),
        sa.UniqueConstraint("id", name=op.f("uq_book_id")),
    )
    op.create_table(
        "borrow",
        sa.Column("reader_name", sa.String(length=100), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("borrow_date", sa.Date(), nullable=False),
        sa.Column("return_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["book.id"], name=op.f("fk_borrow_book_id_book")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_borrow")),
        sa.UniqueConstraint("id", name=op.f("uq_borrow_id")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("borrow")
    op.drop_table("book")
    op.drop_table("author")
    # ### end Alembic commands ###