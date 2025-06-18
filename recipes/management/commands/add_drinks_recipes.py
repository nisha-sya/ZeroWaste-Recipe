from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds drinks recipes to the database'

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

        # Get drinks category
        drinks_category, created = Category.objects.get_or_create(
            name='Drinks',
            defaults={'slug': 'drinks'}
        )

        # Recipe data
        drinks_recipes = [
            {
                'title': 'Iced Matcha Latte',
                'description': 'Chilled green tea latte with milk — refreshing and antioxidant-rich.',
                'cooking_time': 5,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Matcha powder', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Hot water', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Milk', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Honey', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Ice cubes', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Vanilla extract', 'quantity': '1/4', 'unit': 'tsp'},
                ],
                'steps': [
                    'Sift matcha powder into a bowl.',
                    'Add hot water and whisk until smooth and frothy.',
                    'Heat milk in a saucepan or microwave.',
                    'Add honey and vanilla to hot milk, stir well.',
                    'Pour matcha mixture into serving glasses.',
                    'Add ice cubes to glasses.',
                    'Slowly pour milk over ice.',
                    'Stir gently and serve immediately.',
                ]
            },
            {
                'title': 'Lassi',
                'description': 'Yogurt-based drink in sweet or salty version — cooling and probiotic.',
                'cooking_time': 5,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Plain yogurt', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Water', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Sugar', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Cardamom powder', 'quantity': '1/4', 'unit': 'tsp'},
                    {'name': 'Rose water', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Ice cubes', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Saffron strands', 'quantity': '1', 'unit': 'pinch'},
                ],
                'steps': [
                    'Soak saffron in 1 tablespoon warm water.',
                    'Blend yogurt, water, and sugar until smooth.',
                    'Add cardamom powder and rose water.',
                    'Stir in saffron water for color and flavor.',
                    'Add ice cubes and blend briefly.',
                    'Pour into serving glasses.',
                    'Garnish with a few saffron strands.',
                    'Serve chilled and refreshing.',
                ]
            },
            {
                'title': 'Fresh Lemon Mint Cooler',
                'description': 'Zesty lemonade blended with mint leaves — perfect for summer.',
                'cooking_time': 10,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Fresh lemons', 'quantity': '6', 'unit': 'large'},
                    {'name': 'Fresh mint leaves', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Sugar', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Water', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Ice cubes', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Lemon slices', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Mint sprigs', 'quantity': '4', 'unit': 'pieces'},
                ],
                'steps': [
                    'Juice lemons to get fresh lemon juice.',
                    'Make simple syrup by heating water and sugar.',
                    'Muddle fresh mint leaves in a pitcher.',
                    'Add lemon juice and cooled simple syrup.',
                    'Fill pitcher with cold water and stir well.',
                    'Add ice cubes to serving glasses.',
                    'Pour lemon mint cooler over ice.',
                    'Garnish with lemon slices and mint sprigs.',
                ]
            },
            {
                'title': 'Espresso Macchiato',
                'description': 'Strong espresso topped with a dash of foamed milk.',
                'cooking_time': 5,
                'servings': 1,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Espresso beans', 'quantity': '18', 'unit': 'grams'},
                    {'name': 'Fresh milk', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Filtered water', 'quantity': '2', 'unit': 'oz'},
                    {'name': 'Sugar', 'quantity': '1', 'unit': 'tsp'},
                ],
                'steps': [
                    'Grind espresso beans to fine consistency.',
                    'Tamp ground coffee firmly in portafilter.',
                    'Extract espresso shot for 25-30 seconds.',
                    'Steam milk to create microfoam.',
                    'Pour espresso into preheated cup.',
                    'Add a small amount of foamed milk on top.',
                    'Serve immediately while hot.',
                    'Add sugar to taste if desired.',
                ]
            },
            {
                'title': 'Mixed Berries Smoothie',
                'description': 'Nutrient-rich smoothie with yogurt or almond milk base.',
                'cooking_time': 5,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Mixed berries', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Banana', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Greek yogurt', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Almond milk', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Honey', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Chia seeds', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Ice cubes', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Vanilla extract', 'quantity': '1/2', 'unit': 'tsp'},
                ],
                'steps': [
                    'Wash and prepare fresh mixed berries.',
                    'Peel and slice banana into chunks.',
                    'Add all ingredients to blender.',
                    'Blend on high speed until smooth.',
                    'Add more almond milk if too thick.',
                    'Taste and adjust sweetness with honey.',
                    'Pour into serving glasses.',
                    'Garnish with fresh berries and serve immediately.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in drinks_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=drinks_category,
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
            self.style.SUCCESS('Drinks recipes added successfully!')
        ) 