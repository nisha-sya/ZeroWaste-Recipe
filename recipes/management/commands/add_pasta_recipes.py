from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds pasta & noodles recipes to the database'

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

        # Get pasta & noodles category
        pasta_category, created = Category.objects.get_or_create(
            name='Pasta & Noodles',
            defaults={'slug': 'pasta-noodles'}
        )

        # Recipe data
        pasta_recipes = [
            {
                'title': 'Penne Arrabbiata',
                'description': 'Penne pasta in a spicy tomato-garlic chili sauce — bold and flavorful.',
                'cooking_time': 25,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Penne pasta', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Tomatoes', 'quantity': '2', 'unit': 'lbs'},
                    {'name': 'Garlic', 'quantity': '6', 'unit': 'cloves'},
                    {'name': 'Red chili flakes', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Olive oil', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Fresh basil', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Parmesan cheese', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Cook penne pasta in salted water until al dente.',
                    'Sauté minced garlic in olive oil until golden.',
                    'Add crushed tomatoes and red chili flakes.',
                    'Simmer sauce for 15 minutes until thickened.',
                    'Toss cooked pasta with spicy tomato sauce.',
                    'Garnish with fresh basil and grated parmesan.',
                    'Serve immediately while hot.',
                ]
            },
            {
                'title': 'Pad Thai',
                'description': 'Stir-fried rice noodles with tamarind sauce, eggs, tofu or shrimp, peanuts, and lime.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Rice noodles', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Tofu', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Eggs', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Bean sprouts', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Tamarind paste', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Fish sauce', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Palm sugar', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Peanuts', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Lime', 'quantity': '2', 'unit': 'pieces'},
                ],
                'steps': [
                    'Soak rice noodles in warm water for 30 minutes.',
                    'Stir-fry tofu until golden brown, set aside.',
                    'Scramble eggs in the same pan, set aside.',
                    'Stir-fry noodles with tamarind, fish sauce, and sugar.',
                    'Add tofu, eggs, and bean sprouts.',
                    'Toss everything together until well combined.',
                    'Garnish with crushed peanuts and lime wedges.',
                ]
            },
            {
                'title': 'Macaroni and Cheese',
                'description': 'Classic comfort food with creamy cheese sauce and baked topping.',
                'cooking_time': 35,
                'servings': 6,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Macaroni pasta', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Cheddar cheese', 'quantity': '3', 'unit': 'cups'},
                    {'name': 'Milk', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Butter', 'quantity': '4', 'unit': 'tbsp'},
                    {'name': 'All-purpose flour', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Breadcrumbs', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Cook macaroni in salted water until al dente.',
                    'Melt butter and whisk in flour to make roux.',
                    'Gradually add milk while whisking constantly.',
                    'Add shredded cheese and stir until melted.',
                    'Mix cheese sauce with cooked macaroni.',
                    'Top with breadcrumbs and bake at 350°F for 20 minutes.',
                    'Serve hot and bubbly.',
                ]
            },
            {
                'title': 'Japchae',
                'description': 'Stir-fried sweet potato noodles with vegetables and soy-based sauce.',
                'cooking_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Sweet potato noodles', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Spinach', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Carrots', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Mushrooms', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Soy sauce', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Sesame oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Sesame seeds', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Sugar', 'quantity': '1', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Soak sweet potato noodles in warm water for 30 minutes.',
                    'Blanch spinach and squeeze out excess water.',
                    'Julienne carrots and slice mushrooms.',
                    'Stir-fry vegetables separately until tender.',
                    'Cook noodles in boiling water for 5 minutes.',
                    'Mix soy sauce, sesame oil, and sugar.',
                    'Toss noodles with vegetables and sauce.',
                    'Garnish with sesame seeds and serve.',
                ]
            },
            {
                'title': 'Pesto Fettuccine',
                'description': 'Fettuccine tossed in fresh basil pesto with cherry tomatoes and parmesan.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Fettuccine pasta', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Fresh basil', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Pine nuts', 'quantity': '1/3', 'unit': 'cup'},
                    {'name': 'Parmesan cheese', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Garlic', 'quantity': '2', 'unit': 'cloves'},
                    {'name': 'Olive oil', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Cherry tomatoes', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Lemon juice', 'quantity': '1', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Cook fettuccine in salted water until al dente.',
                    'Blend basil, pine nuts, parmesan, garlic, and olive oil.',
                    'Add lemon juice and season pesto to taste.',
                    'Toss hot pasta with fresh pesto.',
                    'Add halved cherry tomatoes.',
                    'Serve immediately with extra parmesan.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in pasta_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=pasta_category,
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
            self.style.SUCCESS('Pasta & noodles recipes added successfully!')
        ) 