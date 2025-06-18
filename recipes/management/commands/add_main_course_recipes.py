from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds main course recipes to the database'

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

        # Get main course category
        main_course_category, created = Category.objects.get_or_create(
            name='Main Course',
            defaults={'slug': 'main-course'}
        )

        # Recipe data
        main_course_recipes = [
            {
                'title': 'Teriyaki Salmon with Rice',
                'description': 'Grilled salmon glazed with sweet teriyaki sauce, served with fluffy white rice.',
                'cooking_time': 25,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Salmon fillets', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Soy sauce', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Brown sugar', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Rice vinegar', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Ginger', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Garlic', 'quantity': '2', 'unit': 'cloves'},
                    {'name': 'White rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Sesame seeds', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Green onions', 'quantity': '2', 'unit': 'stalks'},
                ],
                'steps': [
                    'Cook rice according to package instructions.',
                    'Mix soy sauce, brown sugar, rice vinegar, ginger, and garlic.',
                    'Marinate salmon in teriyaki sauce for 15 minutes.',
                    'Grill salmon for 4-5 minutes per side.',
                    'Brush with remaining teriyaki sauce.',
                    'Serve over rice with sesame seeds and green onions.',
                ]
            },
            {
                'title': 'Spaghetti Carbonara',
                'description': 'Classic Italian pasta with eggs, cheese, pancetta, and black pepper.',
                'cooking_time': 20,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Spaghetti', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Pancetta', 'quantity': '8', 'unit': 'oz'},
                    {'name': 'Eggs', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Parmesan cheese', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Black pepper', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Salt', 'quantity': 'to taste', 'unit': ''},
                ],
                'steps': [
                    'Cook spaghetti in salted water until al dente.',
                    'Fry pancetta until crispy in olive oil.',
                    'Beat eggs with grated parmesan and black pepper.',
                    'Drain pasta, reserving 1 cup of pasta water.',
                    'Quickly toss hot pasta with egg mixture.',
                    'Add pancetta and pasta water if needed.',
                    'Serve immediately with extra parmesan.',
                ]
            },
            {
                'title': 'Beef Bulgogi',
                'description': 'Korean marinated beef grilled to perfection with sweet and savory flavors.',
                'cooking_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Beef sirloin', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Soy sauce', 'quantity': '1/3', 'unit': 'cup'},
                    {'name': 'Brown sugar', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Sesame oil', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Garlic', 'quantity': '4', 'unit': 'cloves'},
                    {'name': 'Ginger', 'quantity': '1', 'unit': 'tbsp'},
                    {'name': 'Asian pear', 'quantity': '1/2', 'unit': 'medium'},
                    {'name': 'Green onions', 'quantity': '3', 'unit': 'stalks'},
                    {'name': 'Sesame seeds', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Slice beef thinly against the grain.',
                    'Blend soy sauce, sugar, sesame oil, garlic, ginger, and pear.',
                    'Marinate beef for at least 2 hours or overnight.',
                    'Grill or pan-fry beef until cooked through.',
                    'Garnish with green onions and sesame seeds.',
                    'Serve with rice and kimchi.',
                ]
            },
            {
                'title': 'Chicken Biryani',
                'description': 'Aromatic Indian rice dish with tender chicken and fragrant spices.',
                'cooking_time': 60,
                'servings': 6,
                'difficulty': 'hard',
                'ingredients': [
                    {'name': 'Chicken thighs', 'quantity': '2', 'unit': 'lbs'},
                    {'name': 'Basmati rice', 'quantity': '3', 'unit': 'cups'},
                    {'name': 'Onions', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Yogurt', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Biryani masala', 'quantity': '3', 'unit': 'tbsp'},
                    {'name': 'Saffron', 'quantity': '1', 'unit': 'pinch'},
                    {'name': 'Ghee', 'quantity': '4', 'unit': 'tbsp'},
                    {'name': 'Mint leaves', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Cilantro', 'quantity': '1/2', 'unit': 'cup'},
                ],
                'steps': [
                    'Marinate chicken with yogurt and biryani masala.',
                    'Soak saffron in warm milk.',
                    'Parboil rice until 70% cooked.',
                    'Layer chicken, rice, and saffron milk in a pot.',
                    'Add mint and cilantro between layers.',
                    'Cook on low heat for 30 minutes.',
                    'Let rest for 10 minutes before serving.',
                ]
            },
            {
                'title': 'Stuffed Bell Peppers',
                'description': 'Colorful bell peppers filled with seasoned ground beef and rice.',
                'cooking_time': 45,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Bell peppers', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Ground beef', 'quantity': '1', 'unit': 'lb'},
                    {'name': 'Cooked rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Onion', 'quantity': '1', 'unit': 'medium'},
                    {'name': 'Tomato sauce', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Cheese', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Italian seasoning', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Garlic', 'quantity': '2', 'unit': 'cloves'},
                    {'name': 'Olive oil', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Cut tops off peppers and remove seeds.',
                    'Brown ground beef with onions and garlic.',
                    'Mix beef with rice, tomato sauce, and seasoning.',
                    'Stuff peppers with beef mixture.',
                    'Top with cheese and bake at 375°F for 30 minutes.',
                    'Serve hot with extra tomato sauce.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in main_course_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=main_course_category,
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
            self.style.SUCCESS('Main course recipes added successfully!')
        ) 