from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds soups & stews recipes to the database'

    def handle(self, *args, **kwargs):
        # Get or create admin user
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

        # Get soups & stews category
        soup_category, created = Category.objects.get_or_create(
            name='Soups & Stews',
            defaults={'slug': 'soups-stews'}
        )

        # Recipe data
        soup_recipes = [
            {
                'title': 'Tomato Basil Soup',
                'description': 'Classic creamy tomato soup with fresh basil and a hint of garlic.',
                'cooking_time': 30,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Tomatoes', 'quantity': '2', 'unit': 'lbs'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Garlic', 'quantity': '4', 'unit': 'cloves'},
                    {'name': 'Fresh basil', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Heavy cream', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Vegetable broth', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Chop tomatoes, onion, and garlic.',
                    'Sauté onion and garlic in olive oil.',
                    'Add tomatoes and cook until softened.',
                    'Add vegetable broth and bring to boil.',
                    'Simmer for 20 minutes, then blend until smooth.',
                    'Stir in cream and fresh basil.',
                    'Season with salt and pepper to taste.',
                ]
            },
            {
                'title': 'Creamy Mushroom Soup',
                'description': 'Rich and creamy soup made with fresh mushrooms and herbs.',
                'cooking_time': 35,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Mushrooms', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
                    {'name': 'Butter', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'All-purpose flour', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Chicken broth', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Heavy cream', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Fresh thyme', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Slice mushrooms and dice onion.',
                    'Melt butter and sauté mushrooms until golden.',
                    'Add onion and garlic, cook until softened.',
                    'Sprinkle flour and cook for 1 minute.',
                    'Gradually add chicken broth while stirring.',
                    'Simmer for 15 minutes, then blend until smooth.',
                    'Stir in cream and fresh thyme.',
                    'Season with salt and pepper.',
                ]
            },
            {
                'title': 'Chicken Stew with Vegetables',
                'description': 'Hearty chicken stew loaded with root vegetables and herbs.',
                'cooking_time': 90,
                'servings': 6,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Chicken thighs', 'quantity': '2', 'unit': 'lbs'},
                    {'name': 'Carrots', 'quantity': '4', 'unit': 'medium'},
                    {'name': 'Potatoes', 'quantity': '3', 'unit': 'large'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Celery', 'quantity': '3', 'unit': 'stalks'},
                    {'name': 'Chicken broth', 'quantity': '6', 'unit': 'cups'},
                    {'name': 'Tomato paste', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Fresh rosemary', 'quantity': '2', 'unit': 'sprigs'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Season chicken thighs with salt and pepper.',
                    'Brown chicken in olive oil, then remove.',
                    'Sauté onion, carrots, celery, and potatoes.',
                    'Add chicken broth, tomato paste, and rosemary.',
                    'Return chicken to pot and bring to boil.',
                    'Simmer covered for 45 minutes until chicken is tender.',
                    'Remove rosemary sprigs and serve hot.',
                ]
            },
            {
                'title': 'Lentil and Carrot Soup',
                'description': 'Nutritious and warming soup with red lentils and sweet carrots.',
                'cooking_time': 40,
                'servings': 6,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Red lentils', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Carrots', 'quantity': '6', 'unit': 'medium'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
                    {'name': 'Vegetable broth', 'quantity': '8', 'unit': 'cups'},
                    {'name': 'Cumin', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Coriander', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Lemon juice', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Fresh cilantro', 'quantity': '1/4', 'unit': 'cup'},
                ],
                'steps': [
                    'Rinse lentils thoroughly.',
                    'Dice carrots, onion, and garlic.',
                    'Sauté onion and garlic until fragrant.',
                    'Add carrots and cook for 5 minutes.',
                    'Add lentils, broth, and spices.',
                    'Bring to boil, then simmer for 25 minutes.',
                    'Stir in lemon juice and fresh cilantro.',
                    'Serve hot with crusty bread.',
                ]
            },
            {
                'title': 'Thai Coconut Curry Soup',
                'description': 'Aromatic Thai-inspired soup with coconut milk, curry, and fresh vegetables.',
                'cooking_time': 25,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Coconut milk', 'quantity': '2', 'unit': 'cans'},
                    {'name': 'Vegetable broth', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Red curry paste', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Lemongrass', 'quantity': '2', 'unit': 'stalks'},
                    {'name': 'Ginger', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Mushrooms', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Bamboo shoots', 'quantity': '1', 'unit': 'can'},
                    {'name': 'Lime juice', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Fish sauce', 'quantity': '1', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Heat coconut milk in a large pot.',
                    'Add curry paste and stir until fragrant.',
                    'Add vegetable broth, lemongrass, and ginger.',
                    'Bring to simmer and add mushrooms.',
                    'Add bamboo shoots and cook for 10 minutes.',
                    'Stir in lime juice and fish sauce.',
                    'Remove lemongrass stalks before serving.',
                    'Garnish with fresh cilantro and lime wedges.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in soup_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=soup_category,
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
            else:
                self.stdout.write(
                    self.style.WARNING(f'Recipe "{recipe_data["title"]}" already exists, skipping...')
                )

        self.stdout.write(
            self.style.SUCCESS('Soups & stews recipes added successfully!')
        ) 