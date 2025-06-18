from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds snacks & street food recipes to the database'

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

        # Get snacks & street food category
        snacks_category, created = Category.objects.get_or_create(
            name='Snacks & Street Food',
            defaults={'slug': 'snacks-street-food'}
        )

        # Recipe data
        snacks_recipes = [
            {
                'title': 'Falafel Balls',
                'description': 'Crispy deep-fried chickpea patties served with tahini dip.',
                'cooking_time': 30,
                'servings': 6,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Chickpeas', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Garlic', 'quantity': '4', 'unit': 'cloves'},
                    {'name': 'Fresh parsley', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Cumin', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Coriander', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Baking soda', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Vegetable oil', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Tahini', 'quantity': '1/2', 'unit': 'cup'},
                ],
                'steps': [
                    'Soak chickpeas overnight, drain and rinse.',
                    'Blend chickpeas, onion, garlic, and parsley.',
                    'Add spices and baking soda, mix well.',
                    'Form mixture into small balls or patties.',
                    'Heat oil to 350°F for deep frying.',
                    'Fry falafel until golden brown and crispy.',
                    'Make tahini sauce with tahini, lemon, and water.',
                    'Serve hot with tahini dip and pita bread.',
                ]
            },
            {
                'title': 'Arancini',
                'description': 'Fried rice balls stuffed with cheese or meat, coated with breadcrumbs.',
                'cooking_time': 45,
                'servings': 8,
                'difficulty': 'hard',
                'ingredients': [
                    {'name': 'Arborio rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Chicken broth', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Mozzarella cheese', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Eggs', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Breadcrumbs', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Parmesan cheese', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Saffron', 'quantity': '1', 'unit': 'pinch'},
                    {'name': 'Vegetable oil', 'quantity': '3', 'unit': 'cups'},
                    {'name': 'Marinara sauce', 'quantity': '2', 'unit': 'cups'},
                ],
                'steps': [
                    'Cook risotto with saffron and chicken broth.',
                    'Let risotto cool completely in refrigerator.',
                    'Form rice into balls, stuffing with mozzarella.',
                    'Coat balls in flour, then beaten eggs.',
                    'Roll in breadcrumbs mixed with parmesan.',
                    'Heat oil to 375°F for deep frying.',
                    'Fry arancini until golden and crispy.',
                    'Serve hot with marinara sauce for dipping.',
                ]
            },
            {
                'title': 'Tteokbokki',
                'description': 'Spicy rice cakes cooked in gochujang sauce — chewy and addictive.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Rice cakes', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Fish cakes', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Gochujang', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Gochugaru', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Soy sauce', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Sugar', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
                    {'name': 'Green onions', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Sesame seeds', 'quantity': '1', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Soak rice cakes in warm water for 30 minutes.',
                    'Mix gochujang, gochugaru, soy sauce, and sugar.',
                    'Sauté minced garlic in oil until fragrant.',
                    'Add sauce mixture and water, bring to boil.',
                    'Add rice cakes and fish cakes.',
                    'Simmer until sauce thickens and rice cakes are soft.',
                    'Garnish with green onions and sesame seeds.',
                    'Serve hot and spicy.',
                ]
            },
            {
                'title': 'Empanadas',
                'description': 'Pastry pockets filled with spiced meat, cheese, or vegetables.',
                'cooking_time': 60,
                'servings': 12,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'All-purpose flour', 'quantity': '3', 'unit': 'cups'},
                    {'name': 'Butter', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Ground beef', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Bell peppers', 'quantity': '2', 'unit': 'medium'},
                    {'name': 'Cumin', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Paprika', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Eggs', 'quantity': '1', 'unit': 'large'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Make pastry dough with flour, butter, and cold water.',
                    'Refrigerate dough for 30 minutes.',
                    'Sauté ground beef with onions and peppers.',
                    'Add spices and cook until meat is browned.',
                    'Roll out dough and cut into circles.',
                    'Fill each circle with meat mixture.',
                    'Fold and crimp edges to seal.',
                    'Brush with beaten egg and bake at 375°F for 25 minutes.',
                ]
            },
            {
                'title': 'French Fries with Truffle Aioli',
                'description': 'Crispy fries tossed in herbs, served with truffle-infused aioli.',
                'cooking_time': 35,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Russet potatoes', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Vegetable oil', 'quantity': '4', 'unit': 'cups'},
                    {'name': 'Mayonnaise', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Truffle oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Lemon juice', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Garlic', 'quantity': '2', 'unit': 'cloves'},
                    {'name': 'Fresh herbs', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Salt and pepper', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Cut potatoes into uniform fry shapes.',
                    'Soak fries in cold water for 30 minutes.',
                    'Drain and pat dry completely.',
                    'Heat oil to 325°F for first fry.',
                    'Fry potatoes for 5 minutes, remove and drain.',
                    'Increase oil temperature to 375°F.',
                    'Fry again until golden and crispy.',
                    'Make aioli with mayo, truffle oil, lemon, and garlic.',
                    'Toss fries with herbs and serve with aioli.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in snacks_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=snacks_category,
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
            self.style.SUCCESS('Snacks & street food recipes added successfully!')
        ) 