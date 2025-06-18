from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds specific breakfast recipes to the database'

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

        # Get breakfast category
        breakfast_category, created = Category.objects.get_or_create(
            name='Breakfast',
            defaults={'slug': 'breakfast'}
        )

        # Recipe data
        breakfast_recipes = [
            {
                'title': 'Vegetable Omelette with Toast',
                'description': 'A healthy and delicious omelette filled with fresh vegetables, served with crispy toast.',
                'cooking_time': 15,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Eggs', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Bell peppers', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Onion', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Tomatoes', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Spinach', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Bread', 'quantity': '4', 'unit': 'slices'},
                    {'name': 'Butter', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Salt', 'quantity': 'to taste', 'unit': ''},
                    {'name': 'Black pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Chop all vegetables finely.',
                    'Beat eggs in a bowl and season with salt and pepper.',
                    'Heat butter in a non-stick pan over medium heat.',
                    'Add vegetables and sauté for 2-3 minutes.',
                    'Pour beaten eggs over vegetables.',
                    'Cook until eggs are set, folding in half.',
                    'Toast bread and serve with omelette.',
                ]
            },
            {
                'title': 'Banana Pancakes with Honey',
                'description': 'Fluffy pancakes made with ripe bananas and drizzled with golden honey.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'All-purpose flour', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Ripe bananas', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Milk', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Egg', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Sugar', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Baking powder', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Salt', 'quantity': '1/4', 'unit': 'tsp'},
                    {'name': 'Honey', 'quantity': 'to taste', 'unit': ''},
                    {'name': 'Butter', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Mash bananas in a large bowl until smooth.',
                    'Add egg, milk, and sugar to mashed bananas.',
                    'In another bowl, mix flour, baking powder, and salt.',
                    'Combine wet and dry ingredients, mixing gently.',
                    'Heat butter in a pan over medium heat.',
                    'Pour 1/4 cup batter for each pancake.',
                    'Cook until bubbles form, then flip.',
                    'Serve with honey drizzled on top.',
                ]
            },
            {
                'title': 'Tamago Kake Gohan',
                'description': 'A traditional Japanese breakfast dish with raw egg over hot rice.',
                'cooking_time': 10,
                'servings': 1,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Cooked rice', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Fresh egg', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Soy sauce', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Green onions', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Nori (seaweed)', 'quantity': '1', 'unit': 'sheet'},
                    {'name': 'Sesame seeds', 'quantity': '1', 'unit': 'tsp'},
                ],
                'steps': [
                    'Place hot rice in a bowl.',
                    'Crack a fresh egg over the rice.',
                    'Add soy sauce to taste.',
                    'Mix gently with chopsticks.',
                    'Top with chopped green onions.',
                    'Sprinkle with sesame seeds.',
                    'Serve with nori on the side.',
                ]
            },
            {
                'title': 'Feta Cheese with Olives and Cucumbers',
                'description': 'A refreshing plate of crumbled feta, kalamata olives, and sliced cucumber.',
                'cooking_time': 5,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Feta cheese', 'quantity': '200', 'unit': 'g'},
                    {'name': 'Kalamata olives', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Cucumber', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Lemon juice', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Dried oregano', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Black pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Slice cucumber into thin rounds.',
                    'Crumble feta cheese into a bowl.',
                    'Add olives and cucumber slices.',
                    'Drizzle with olive oil and lemon juice.',
                    'Sprinkle with oregano and black pepper.',
                    'Toss gently to combine.',
                    'Serve immediately.',
                ]
            },
            {
                'title': 'Hummus & Pita',
                'description': 'Creamy chickpea dip paired with warm pita bread — simple and protein-packed.',
                'cooking_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Chickpeas', 'quantity': '1', 'unit': 'can'},
                    {'name': 'Tahini', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Lemon juice', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Garlic', 'quantity': '2', 'unit': 'cloves'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Cumin', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Salt', 'quantity': 'to taste', 'unit': ''},
                    {'name': 'Pita bread', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Paprika', 'quantity': '1', 'unit': 'tsp'},
                ],
                'steps': [
                    'Drain and rinse chickpeas.',
                    'Blend chickpeas, tahini, lemon juice, and garlic.',
                    'Add olive oil and cumin while blending.',
                    'Season with salt to taste.',
                    'Transfer to serving bowl.',
                    'Drizzle with olive oil and sprinkle paprika.',
                    'Warm pita bread and serve.',
                ]
            },
            {
                'title': 'Date & Nut Energy Balls',
                'description': 'Naturally sweet bites made with dates, almonds, and sesame — great for a light start or side.',
                'cooking_time': 20,
                'servings': 12,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Dates', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Almonds', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Sesame seeds', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Coconut flakes', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Cinnamon', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Vanilla extract', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Coconut oil', 'quantity': '1', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Soak dates in warm water for 10 minutes.',
                    'Process almonds in food processor until fine.',
                    'Add dates and process until mixture forms a ball.',
                    'Add sesame seeds, coconut, cinnamon, and vanilla.',
                    'Process until well combined.',
                    'Roll mixture into small balls.',
                    'Refrigerate for 30 minutes before serving.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in breakfast_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=breakfast_category,
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
            self.style.SUCCESS('Breakfast recipes added successfully!')
        ) 