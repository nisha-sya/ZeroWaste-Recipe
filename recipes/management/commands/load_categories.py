from django.core.management.base import BaseCommand
from recipes.models import Category

class Command(BaseCommand):
    help = 'Loads initial recipe categories'

    def handle(self, *args, **kwargs):
        categories = [
            'Breakfast',
            'Main Course',
            'Healthy & Vegetarian',
            'Soups & Stews',
            'Pasta & Noodles',
            'Rice-Based',
            'Snacks & Street Food',
            'Desserts',
            'Drinks'
        ]

        for category_name in categories:
            Category.objects.get_or_create(
                name=category_name,
                defaults={
                    'description': f'Collection of {category_name.lower()} recipes from around the world'
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category_name}"')
            ) 