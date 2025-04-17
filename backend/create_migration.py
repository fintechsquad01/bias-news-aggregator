"""
Script to create initial migration revision.
"""
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from alembic import command
from alembic.config import Config

# Get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, ".."))

# Create Alembic configuration
alembic_cfg = Config(os.path.join(parent_dir, "alembic.ini"))
alembic_cfg.set_main_option("script_location", "app/db/migrations")

# Create initial migration
command.revision(alembic_cfg, autogenerate=True, message="Initial migration")

print("Initial migration created.")
