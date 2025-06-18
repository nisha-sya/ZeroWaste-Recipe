#!/usr/bin/env python
"""
Management script for production deployment.
This script shows how to run Django with production settings.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Run Django with production settings."""
    # Set the Django settings module to production
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReceipeApp.production')
    
    # Initialize Django
    django.setup()
    
    # Execute the management command
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main() 