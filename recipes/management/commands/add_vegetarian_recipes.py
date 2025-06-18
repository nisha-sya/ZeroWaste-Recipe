from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds healthy & vegetarian recipes to the database'

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

        # Get healthy & vegetarian category
        vegetarian_category, created = Category.objects.get_or_create(
            name='Healthy & Vegetarian',
            defaults={'slug': 'healthy-vegetarian'}
        )

        # Recipe data
        vegetarian_recipes = [
            {
                'title': 'Quinoa Salad with Chickpeas',
                'description': 'Nutritious quinoa salad packed with protein-rich chickpeas and fresh vegetables.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Quinoa', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Chickpeas', 'quantity': '1', 'unit': 'can'},
                    {'name': 'Cucumber', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Cherry tomatoes', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Red onion', 'quantity': '1/2', 'unit': 'medium'},
                    {'name': 'Lemon juice', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Fresh parsley', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Rinse quinoa and cook according to package instructions.',
                    'Drain and rinse chickpeas.',
                    'Chop cucumber, tomatoes, and red onion.',
                    'Mix quinoa with vegetables and chickpeas.',
                    'Whisk lemon juice, olive oil, salt, and pepper.',
                    'Pour dressing over salad and toss gently.',
                    'Garnish with fresh parsley and serve.',
                ]
            },
            {
                'title': 'Grilled Vegetable Wrap',
                'description': 'Fresh grilled vegetables wrapped in a whole wheat tortilla with hummus.',
                'cooking_time': 15,
                'servings': 2,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Whole wheat tortillas', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Zucchini', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Bell peppers', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Eggplant', 'quantity': '1/2', 'unit': 'medium'},
                    {'name': 'Hummus', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Mixed greens', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Balsamic vinegar', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Slice vegetables into thin strips.',
                    'Brush vegetables with olive oil and season.',
                    'Grill vegetables until tender and charred.',
                    'Warm tortillas slightly.',
                    'Spread hummus on tortillas.',
                    'Layer grilled vegetables and greens.',
                    'Drizzle with balsamic and roll up.',
                ]
            },
            {
                'title': 'Spinach and Tofu Stir Fry',
                'description': 'Quick and healthy stir fry with fresh spinach and protein-rich tofu.',
                'cooking_time': 15,
                'servings': 3,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Firm tofu', 'quantity': '1', 'unit': 'block'},
                    {'name': 'Fresh spinach', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
                    {'name': 'Ginger', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Soy sauce', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Sesame oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Red pepper flakes', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Sesame seeds', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Brown rice', 'quantity': '2', 'unit': 'cups'},
                ],
                'steps': [
                    'Press tofu to remove excess water and cube.',
                    'Cook brown rice according to package instructions.',
                    'Heat sesame oil in a wok or large pan.',
                    'Stir fry tofu until golden brown.',
                    'Add garlic, ginger, and red pepper flakes.',
                    'Add spinach and stir fry until wilted.',
                    'Season with soy sauce and sesame seeds.',
                    'Serve over brown rice.',
                ]
            },
            {
                'title': 'Lentil Soup with Whole Wheat Bread',
                'description': 'Hearty lentil soup packed with protein and fiber, served with whole wheat bread.',
                'cooking_time': 45,
                'servings': 6,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Red lentils', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Carrots', 'quantity': '3', 'unit': 'medium'},
                    {'name': 'Celery', 'quantity': '2', 'unit': 'stalks'},
                    {'name': 'Garlic', 'quantity': '4', 'unit': 'cloves'},
                    {'name': 'Vegetable broth', 'quantity': '6', 'unit': 'cups'},
                    {'name': 'Cumin', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Turmeric', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Whole wheat bread', 'quantity': '1', 'unit': 'loaf'},
                ],
                'steps': [
                    'Rinse lentils thoroughly.',
                    'Sauté onion, carrots, celery, and garlic.',
                    'Add lentils, broth, and spices.',
                    'Bring to boil, then simmer for 30 minutes.',
                    'Stir occasionally until lentils are tender.',
                    'Season with salt and pepper to taste.',
                    'Serve hot with whole wheat bread.',
                ]
            },
            {
                'title': 'Zucchini Noodles with Pesto',
                'description': 'Light and fresh zucchini noodles tossed with homemade basil pesto.',
                'cooking_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Zucchini', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Fresh basil', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Pine nuts', 'quantity': '1/3', 'unit': 'cup'},
                    {'name': 'Parmesan cheese', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Garlic', 'quantity': '2', 'unit': 'cloves'},
                    {'name': 'Olive oil', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Lemon juice', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Cherry tomatoes', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Spiralize zucchini into noodles.',
                    'Blend basil, pine nuts, parmesan, garlic, and olive oil.',
                    'Add lemon juice and season pesto.',
                    'Toss zucchini noodles with pesto.',
                    'Add halved cherry tomatoes.',
                    'Serve immediately while fresh.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in vegetarian_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=vegetarian_category,
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
            self.style.SUCCESS('Healthy & vegetarian recipes added successfully!')
        ) 