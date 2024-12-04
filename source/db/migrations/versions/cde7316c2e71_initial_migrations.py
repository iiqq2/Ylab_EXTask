"""initial migrations

Revision ID: cde7316c2e71
Revises:
Create Date: 2024-12-04 15:11:28.032971

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cde7316c2e71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deferred_tasks',
                    sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
                    sa.Column('topic', sa.String(), nullable=False),
                    sa.Column('key', sa.String(), nullable=False),
                    sa.Column('value', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('menus',
                    sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('submenus',
                    sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('menu_id', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('dishes',
                    sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('price', sa.Numeric(precision=30, scale=28), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('submenu_id', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('submenus')
    op.drop_table('menus')
    op.drop_table('deferred_tasks')
    # ### end Alembic commands ###