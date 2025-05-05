"""Add sentiment_confidence and bias_score to Article model

Revision ID: 55a9e52eda7b
Revises: 
Create Date: 2024-04-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55a9e52eda7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add sentiment_confidence and bias_score columns to articles table
    op.add_column('articles', sa.Column('sentiment_confidence', sa.Float(), nullable=True))
    op.add_column('articles', sa.Column('bias_score', sa.Float(), nullable=True))


def downgrade():
    # Remove sentiment_confidence and bias_score columns from articles table
    op.drop_column('articles', 'sentiment_confidence')
    op.drop_column('articles', 'bias_score') 