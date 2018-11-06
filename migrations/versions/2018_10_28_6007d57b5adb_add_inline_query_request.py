"""Add inline query request

Revision ID: 6007d57b5adb
Revises: f8f6a6d47d96
Create Date: 2018-10-28 01:20:20.467816

"""
from alembic import op
import sqlalchemy as sa
import os
import sys
from sqlalchemy.orm.session import Session

# Set system path, so alembic is capable of finding the stickerfinder module
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "stickerfinder"))
sys.path.append(parent_dir)

from stickerfinder.models import * # noqa


# revision identifiers, used by Alembic.
revision = '6007d57b5adb'
down_revision = 'f8f6a6d47d96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'inline_query_request',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('offset', sa.String(), nullable=True),
        sa.Column('duration', sa.Interval(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('inline_query_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['inline_query_id'], ['inline_query.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inline_query_request_inline_query_id'), 'inline_query_request', ['inline_query_id'], unique=False)
    # ### end Alembic commands ###

    session = Session(bind=op.get_bind())
    inline_queries = session.query(InlineQuery) \
        .order_by(InlineQuery.created_at.asc()) \
        .all()

    last_inline_query = None
    for inline_query in inline_queries:
        if last_inline_query is None:
            last_inline_query = inline_query
            inline_query_request = InlineQueryRequest(inline_query, inline_query.offset, inline_query.duration)
            session.add(inline_query_request)

        elif inline_query.query == last_inline_query.query:
            if session.query(InlineQueryRequest) \
                    .filter(InlineQueryRequest.inline_query_id == last_inline_query.id) \
                    .filter(InlineQueryRequest.offset == inline_query.offset) \
                    .one_or_none():
                inline_query_request = InlineQueryRequest(inline_query, inline_query.offset, inline_query.duration)
                last_inline_query = inline_query
            else:
                inline_query_request = InlineQueryRequest(last_inline_query, inline_query.offset, inline_query.duration)
                session.delete(inline_query)
            session.add(inline_query_request)

        elif inline_query.query != last_inline_query.query:
            last_inline_query = inline_query
            inline_query_request = InlineQueryRequest(inline_query, inline_query.offset, inline_query.duration)
            session.add(inline_query_request)

    session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_inline_query_request_inline_query_id'), table_name='inline_query_request')
    op.drop_table('inline_query_request')
    # ### end Alembic commands ###
