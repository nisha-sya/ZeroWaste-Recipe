from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Step, Category

# Create your tests here.

class RecipeFormsetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_add_recipe_with_ingredients_and_steps(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('recipes:add_recipe')
        data = {
            'title': 'Test Recipe',
            'description': 'A test recipe.',
            'category': self.category.id,
            'cooking_time': 30,
            'servings': 2,
            'is_featured': True,
            'is_published': True,
            # Ingredient formset management
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': 'Flour',
            'ingredients-0-quantity': '2',
            'ingredients-0-unit': 'cups',
            'ingredients-1-name': 'Sugar',
            'ingredients-1-quantity': '1',
            'ingredients-1-unit': 'cup',
            # Step formset management
            'steps-TOTAL_FORMS': '2',
            'steps-INITIAL_FORMS': '0',
            'steps-MIN_NUM_FORMS': '0',
            'steps-MAX_NUM_FORMS': '1000',
            'steps-0-order': '1',
            'steps-0-description': 'Mix ingredients.',
            'steps-1-order': '2',
            'steps-1-description': 'Bake for 30 minutes.',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        recipe = Recipe.objects.get(title='Test Recipe')
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(recipe.steps.count(), 2)
        self.assertEqual(recipe.ingredients.first().name, 'Flour')
        self.assertEqual(recipe.steps.first().description, 'Mix ingredients.')

    def test_edit_recipe_add_ingredient(self):
        self.client.login(username='testuser', password='testpass')
        recipe = Recipe.objects.create(
            title='Edit Recipe',
            description='Edit test',
            category=self.category,
            cooking_time=10,
            servings=1,
            author=self.user,
            is_published=True
        )
        Ingredient.objects.create(recipe=recipe, name='Salt', quantity='1', unit='tsp')
        Step.objects.create(recipe=recipe, order=1, description='Add salt.')
        url = reverse('recipes:edit_recipe', args=[recipe.slug])
        data = {
            'title': 'Edit Recipe',
            'description': 'Edit test',
            'category': self.category.id,
            'cooking_time': 10,
            'servings': 1,
            'is_featured': False,
            'is_published': True,
            # Ingredient formset
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '1',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-id': recipe.ingredients.first().id,
            'ingredients-0-name': 'Salt',
            'ingredients-0-quantity': '1',
            'ingredients-0-unit': 'tsp',
            'ingredients-1-name': 'Pepper',
            'ingredients-1-quantity': '1',
            'ingredients-1-unit': 'tsp',
            # Step formset
            'steps-TOTAL_FORMS': '1',
            'steps-INITIAL_FORMS': '1',
            'steps-MIN_NUM_FORMS': '0',
            'steps-MAX_NUM_FORMS': '1000',
            'steps-0-id': recipe.steps.first().id,
            'steps-0-order': '1',
            'steps-0-description': 'Add salt.',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        recipe.refresh_from_db()
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertTrue(recipe.ingredients.filter(name='Pepper').exists())
