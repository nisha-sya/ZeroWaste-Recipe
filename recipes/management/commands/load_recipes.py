from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify
from .recipe_data import RECIPES_DATA

class Command(BaseCommand):
    help = 'Loads initial recipes'

    def handle(self, *args, **kwargs):
        # Create a superuser if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        for category_name, recipes in RECIPES_DATA.items():
            try:
                category = Category.objects.get(name=category_name)
                
                for recipe_data in recipes:
                    # Create recipe
                    recipe = Recipe.objects.create(
                        title=recipe_data['title'],
                        slug=slugify(recipe_data['title']),
                        description=recipe_data['description'],
                        cooking_time=recipe_data['cooking_time'],
                        servings=recipe_data['servings'],
                        difficulty=recipe_data['difficulty'],
                        category=category,
                        author=admin_user,
                        is_published=True
                    )

                    # Add ingredients
                    for ingredient_data in recipe_data['ingredients']:
                        Ingredient.objects.create(
                            recipe=recipe,
                            name=ingredient_data['name'],
                            quantity=ingredient_data['quantity'],
                            unit=ingredient_data['unit']
                        )

                    # Add steps
                    for i, step_text in enumerate(recipe_data['steps'], 1):
                        Step.objects.create(
                            recipe=recipe,
                            order=i,
                            description=step_text
                        )

                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created recipe "{recipe.title}"')
                    )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Category "{category_name}" does not exist. Please run load_categories first.')
                ) 