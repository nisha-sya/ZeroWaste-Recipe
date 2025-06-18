#!/usr/bin/env python
import os
import sys
import datetime
import subprocess
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReceipeApp.settings')
import django
django.setup()

from django.conf import settings

def backup_database():
    """Create a backup of the PostgreSQL database."""
    # Create backups directory if it doesn't exist
    backup_dir = project_root / 'backups'
    backup_dir.mkdir(exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'backup_{timestamp}.sql'

    # Get database settings
    db_settings = settings.DATABASES['default']
    
    # Construct pg_dump command
    pg_dump_cmd = [
        'pg_dump',
        f'--dbname={db_settings["NAME"]}',
        f'--username={db_settings["USER"]}',
        f'--host={db_settings["HOST"]}',
        f'--port={db_settings["PORT"]}',
        '--format=custom',  # Use custom format for better compression
        '--blobs',  # Include large objects
        '--verbose',  # Show progress
        f'--file={backup_file}',
    ]

    # Set PGPASSWORD environment variable
    os.environ['PGPASSWORD'] = db_settings['PASSWORD']

    try:
        # Execute pg_dump
        subprocess.run(pg_dump_cmd, check=True)
        print(f"Database backup created successfully: {backup_file}")
        
        # Keep only the last 5 backups
        backups = sorted(backup_dir.glob('backup_*.sql'))
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                old_backup.unlink()
                print(f"Deleted old backup: {old_backup}")
                
    except subprocess.CalledProcessError as e:
        print(f"Error creating database backup: {e}")
        sys.exit(1)
    finally:
        # Clear PGPASSWORD from environment
        os.environ.pop('PGPASSWORD', None)

if __name__ == '__main__':
    backup_database() 