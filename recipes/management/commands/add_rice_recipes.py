from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds rice-based recipes to the database'

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

        # Get rice-based category
        rice_category, created = Category.objects.get_or_create(
            name='Rice-Based',
            defaults={'slug': 'rice-based'}
        )

        # Recipe data
        rice_recipes = [
            {
                'title': 'Bibimbap',
                'description': 'Mixed rice bowl with vegetables, fried egg, gochujang (chili paste), and optional meat.',
                'cooking_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Jasmine rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Spinach', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Carrots', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Zucchini', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Bean sprouts', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Eggs', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Gochujang', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Sesame oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Soy sauce', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Cook rice according to package instructions.',
                    'Blanch spinach and season with sesame oil and salt.',
                    'Julienne carrots and zucchini, stir-fry separately.',
                    'Blanch bean sprouts and season.',
                    'Fry eggs sunny-side up.',
                    'Arrange rice in bowls, top with vegetables in sections.',
                    'Place fried egg in center, add gochujang.',
                    'Mix everything together before eating.',
                ]
            },
            {
                'title': 'Paella',
                'description': 'Saffron-flavored rice cooked with seafood, chicken, and vegetables.',
                'cooking_time': 45,
                'servings': 6,
                'difficulty': 'hard',
                'ingredients': [
                    {'name': 'Arborio rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Chicken thighs', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Shrimp', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Mussels', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Saffron threads', 'quantity': '1', 'unit': 'pinch'},
                    {'name': 'Chicken broth', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Tomatoes', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Bell peppers', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Peas', 'quantity': '1', 'unit': 'cup'},
                ],
                'steps': [
                    'Heat olive oil in paella pan, brown chicken pieces.',
                    'Add chopped vegetables and sauté until soft.',
                    'Stir in rice and saffron, cook for 2 minutes.',
                    'Add hot chicken broth and bring to boil.',
                    'Reduce heat and simmer for 20 minutes.',
                    'Add seafood in the last 10 minutes.',
                    'Let rest for 5 minutes before serving.',
                ]
            },
            {
                'title': 'Mexican Burrito Bowl',
                'description': 'Rice topped with beans, salsa, corn, guacamole, grilled meat, and cheese.',
                'cooking_time': 25,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'White rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Black beans', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Chicken breast', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Corn', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Avocado', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Tomatoes', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Lime', 'quantity': '2', 'unit': 'pieces'},
                    {'name': 'Cheddar cheese', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Sour cream', 'quantity': '1/2', 'unit': 'cup'},
                ],
                'steps': [
                    'Cook rice with lime and cilantro.',
                    'Season and grill chicken breast until cooked.',
                    'Warm black beans with spices.',
                    'Make guacamole with mashed avocado, lime, and salt.',
                    'Dice tomatoes and prepare salsa.',
                    'Assemble bowls with rice base.',
                    'Top with beans, chicken, corn, and toppings.',
                    'Garnish with cheese, sour cream, and lime wedges.',
                ]
            },
            {
                'title': 'Vegetarian Fried Rice',
                'description': 'Stir-fried jasmine rice with eggs, peas, carrots, and soy sauce.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Jasmine rice', 'quantity': '3', 'unit': 'cups'},
                    {'name': 'Eggs', 'quantity': '3', 'unit': 'large'},
                    {'name': 'Carrots', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Peas', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Green onions', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Soy sauce', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Sesame oil', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Vegetable oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
                ],
                'steps': [
                    'Cook rice and let cool completely (preferably overnight).',
                    'Scramble eggs in hot oil, set aside.',
                    'Stir-fry minced garlic until fragrant.',
                    'Add diced carrots and stir-fry for 2 minutes.',
                    'Add rice and break up any clumps.',
                    'Stir in peas and green onions.',
                    'Add soy sauce and sesame oil.',
                    'Return eggs to pan and toss everything together.',
                ]
            },
            {
                'title': 'Jollof Rice',
                'description': 'Spiced tomato-based rice dish with vegetables and meat or fish.',
                'cooking_time': 40,
                'servings': 6,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Long grain rice', 'quantity': '3', 'unit': 'cups'},
                    {'name': 'Tomatoes', 'quantity': '6', 'unit': 'large'},
                    {'name': 'Red bell peppers', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Onions', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Scotch bonnet peppers', 'quantity': '2', 'unit': 'pieces'},
                    {'name': 'Tomato paste', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Curry powder', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Thyme', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Bay leaves', 'quantity': '2', 'unit': 'pieces'},
                ],
                'steps': [
                    'Blend tomatoes, peppers, and onions into smooth paste.',
                    'Heat oil and sauté blended mixture until thickened.',
                    'Add tomato paste and spices, cook for 5 minutes.',
                    'Add washed rice and stir to coat.',
                    'Pour in hot water and bring to boil.',
                    'Reduce heat and simmer covered for 25 minutes.',
                    'Let rest for 10 minutes before fluffing.',
                    'Serve hot with grilled meat or fish.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in rice_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=rice_category,
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
            self.style.SUCCESS('Rice-based recipes added successfully!')
        ) 