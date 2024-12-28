"""add settings table

Revision ID: 001
Revises: 
Create Date: 2023-12-23 00:25:20.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Get database connection and check if table exists
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    
    if 'settings' not in tables:
        # Create settings table only if it doesn't exist
        op.create_table('settings',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('dark_mode', sa.Boolean(), nullable=False, server_default='false'),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
    else:
        # If table exists, verify/update its structure
        # This is where you would add any modifications to the existing table
        # For example:
        # if 'new_column' not in [c['name'] for c in inspector.get_columns('settings')]:
        #     op.add_column('settings', sa.Column('new_column', sa.String()))
        pass


def downgrade():
    # Drop settings table
    op.drop_table('settings')
