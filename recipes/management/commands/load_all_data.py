from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Loads all initial data in the correct order'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading categories...')
        call_command('load_categories')
        
        self.stdout.write('Loading recipes...')
        call_command('load_recipes')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all data!')) 