from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Updates existing recipes to assign a default image if none is set.'

    def handle(self, *args, **kwargs):
        updated_count = 0
        for recipe in Recipe.objects.filter(image=''):
            recipe.image = 'recipes/images/default.jpg'
            recipe.save()
            updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} recipes with a default image.')) 