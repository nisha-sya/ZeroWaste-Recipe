from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Step
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds desserts recipes to the database'

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

        # Get desserts category
        desserts_category, created = Category.objects.get_or_create(
            name='Desserts',
            defaults={'slug': 'desserts'}
        )

        # Recipe data
        desserts_recipes = [
            {
                'title': 'Chocolate Lava Cake',
                'description': 'Molten chocolate center in a soft cake shell, served warm.',
                'cooking_time': 15,
                'servings': 4,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Dark chocolate', 'quantity': '4', 'unit': 'oz'},
                    {'name': 'Butter', 'quantity': '4', 'unit': 'tbsp'},
                    {'name': 'Eggs', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Egg yolks', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Powdered sugar', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'All-purpose flour', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Vanilla extract', 'quantity': '1', 'unit': 'tsp'},
                    {'name': 'Salt', 'quantity': '1/8', 'unit': 'tsp'},
                ],
                'steps': [
                    'Preheat oven to 425°F and butter ramekins.',
                    'Melt chocolate and butter together until smooth.',
                    'Whisk eggs, egg yolks, and vanilla until light.',
                    'Fold chocolate mixture into egg mixture.',
                    'Gently fold in flour and salt.',
                    'Pour batter into prepared ramekins.',
                    'Bake for 12-14 minutes until edges are set.',
                    'Serve immediately while center is still molten.',
                ]
            },
            {
                'title': 'Tiramisu',
                'description': 'Layers of espresso-soaked ladyfingers, mascarpone cream, and cocoa.',
                'cooking_time': 30,
                'servings': 8,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Mascarpone cheese', 'quantity': '16', 'unit': 'oz'},
                    {'name': 'Heavy cream', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Eggs', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Sugar', 'quantity': '3/4', 'unit': 'cup'},
                    {'name': 'Ladyfingers', 'quantity': '24', 'unit': 'pieces'},
                    {'name': 'Espresso', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Cocoa powder', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Vanilla extract', 'quantity': '1', 'unit': 'tsp'},
                ],
                'steps': [
                    'Separate eggs and beat yolks with sugar until pale.',
                    'Fold mascarpone into egg yolk mixture.',
                    'Whip heavy cream until stiff peaks form.',
                    'Gently fold whipped cream into mascarpone mixture.',
                    'Dip ladyfingers in cooled espresso.',
                    'Layer half the ladyfingers in serving dish.',
                    'Spread half the mascarpone mixture over ladyfingers.',
                    'Repeat layers and dust with cocoa powder.',
                    'Refrigerate for at least 4 hours before serving.',
                ]
            },
            {
                'title': 'Mango Sticky Rice',
                'description': 'Sweet coconut sticky rice topped with fresh mango slices.',
                'cooking_time': 45,
                'servings': 4,
                'difficulty': 'easy',
                'ingredients': [
                    {'name': 'Sticky rice', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Coconut milk', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Sugar', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Salt', 'quantity': '1/4', 'unit': 'tsp'},
                    {'name': 'Ripe mangoes', 'quantity': '2', 'unit': 'large'},
                    {'name': 'Sesame seeds', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Pandan leaves', 'quantity': '2', 'unit': 'pieces'},
                ],
                'steps': [
                    'Soak sticky rice in water for 4 hours or overnight.',
                    'Steam rice until tender and translucent.',
                    'Heat coconut milk with sugar, salt, and pandan leaves.',
                    'Pour hot coconut milk over steamed rice.',
                    'Let rice absorb coconut milk for 30 minutes.',
                    'Slice mangoes into thin pieces.',
                    'Serve sticky rice topped with mango slices.',
                    'Sprinkle with toasted sesame seeds.',
                ]
            },
            {
                'title': 'Gulab Jamun',
                'description': 'Deep-fried milk balls soaked in rose-scented sugar syrup.',
                'cooking_time': 40,
                'servings': 12,
                'difficulty': 'hard',
                'ingredients': [
                    {'name': 'Milk powder', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'All-purpose flour', 'quantity': '1/4', 'unit': 'cup'},
                    {'name': 'Baking soda', 'quantity': '1/8', 'unit': 'tsp'},
                    {'name': 'Ghee', 'quantity': '2', 'unit': 'tbsp'},
                    {'name': 'Milk', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Sugar', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Water', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Cardamom pods', 'quantity': '4', 'unit': 'pieces'},
                    {'name': 'Rose water', 'quantity': '1', 'unit': 'tsp'},
                ],
                'steps': [
                    'Mix milk powder, flour, and baking soda.',
                    'Add ghee and milk to form soft dough.',
                    'Shape dough into small smooth balls.',
                    'Heat oil and fry balls until golden brown.',
                    'Make sugar syrup with water, sugar, and cardamom.',
                    'Add rose water to syrup and bring to boil.',
                    'Soak fried balls in hot syrup for 2 hours.',
                    'Serve warm or at room temperature.',
                ]
            },
            {
                'title': 'Cheesecake',
                'description': 'Creamy baked cheesecake with a buttery graham cracker crust.',
                'cooking_time': 90,
                'servings': 12,
                'difficulty': 'medium',
                'ingredients': [
                    {'name': 'Graham crackers', 'quantity': '2', 'unit': 'cups'},
                    {'name': 'Butter', 'quantity': '1/2', 'unit': 'cup'},
                    {'name': 'Cream cheese', 'quantity': '32', 'unit': 'oz'},
                    {'name': 'Sugar', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Eggs', 'quantity': '4', 'unit': 'large'},
                    {'name': 'Vanilla extract', 'quantity': '2', 'unit': 'tsp'},
                    {'name': 'Sour cream', 'quantity': '1', 'unit': 'cup'},
                    {'name': 'Lemon juice', 'quantity': '2', 'unit': 'tbsp'},
                ],
                'steps': [
                    'Preheat oven to 325°F and prepare springform pan.',
                    'Crush graham crackers and mix with melted butter.',
                    'Press mixture into pan bottom and bake for 10 minutes.',
                    'Beat cream cheese and sugar until smooth.',
                    'Add eggs one at a time, beating well after each.',
                    'Mix in vanilla, sour cream, and lemon juice.',
                    'Pour filling over crust and bake for 60 minutes.',
                    'Turn off oven and let cheesecake cool inside for 1 hour.',
                    'Refrigerate for at least 4 hours before serving.',
                ]
            }
        ]

        # Create recipes
        for recipe_data in desserts_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(title=recipe_data['title']).exists():
                recipe = Recipe.objects.create(
                    title=recipe_data['title'],
                    slug=slugify(recipe_data['title']),
                    description=recipe_data['description'],
                    cooking_time=recipe_data['cooking_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category=desserts_category,
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
            self.style.SUCCESS('Desserts recipes added successfully!')
        ) 