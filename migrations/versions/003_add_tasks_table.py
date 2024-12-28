"""Add tasks table

Revision ID: 003
Revises: 001
Create Date: 2024-12-22 23:55:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Get database connection and check if table exists
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    
    if 'tasks' not in tables:
        # Create tasks table only if it doesn't exist
        op.create_table('tasks',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
    else:
        # If table exists, verify/update its structure
        existing_columns = {c['name'] for c in inspector.get_columns('tasks')}
        
        # Add any missing columns
        if 'description' not in existing_columns:
            op.add_column('tasks', sa.Column('description', sa.Text(), nullable=True))
        if 'status' not in existing_columns:
            op.add_column('tasks', sa.Column('status', sa.String(length=50), nullable=False, server_default='TODO'))
        if 'created_at' not in existing_columns:
            op.add_column('tasks', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
        if 'updated_at' not in existing_columns:
            op.add_column('tasks', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))


def downgrade():
    op.drop_table('tasks')
