from django.core.management.base import BaseCommand
from recipes.models import Recipe
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Assigns existing images to their corresponding recipes'

    def handle(self, *args, **kwargs):
        # Mapping of image filenames to recipe titles
        image_mapping = {
            # Breakfast recipes
            'Aloo Paratha.jpg': 'Aloo Paratha',
            'Avocado Toast.jpeg': 'Avocado Toast',
            'Banana Pancakes with Honey.jpeg': 'Banana Pancakes with Honey',
            'Feta Cheese with Olives and Cucumbers.jpg': 'Feta Cheese with Olives and Cucumbers',
            'Date & Nut Energy Balls.jpg': 'Date & Nut Energy Balls',
            'Hummus & Pita.avif': 'Hummus & Pita',
            'Vegetable Omelette with Toast.jpg': 'Vegetable Omelette with Toast',
            'Tamago Kake Gohan.jpg': 'Tamago Kake Gohan',
            'Shakshuka.jpg': 'Shakshuka',
            
            # Main Course recipes
            'Beef Bulgogi.jpg': 'Beef Bulgogi',
            'Chicken Biryani.jpg': 'Chicken Biryani',
            'Chicken Curry.jpg': 'Chicken Curry',
            'Spaghetti Carbonara.jpg': 'Spaghetti Carbonara',
            'Stuffed Bell Peppers.jpg': 'Stuffed Bell Peppers',
            'Teriyaki Salmon with Rice.jpg': 'Teriyaki Salmon with Rice',
            
            # Healthy & Vegetarian recipes
            'Grilled Vegetable Wrap.jpg': 'Grilled Vegetable Wrap',
            'Quinoa Salad.webp': 'Quinoa Salad',
            'Quinoa Salad with Chickpeas.jpg': 'Quinoa Salad',
            'Spinach and Tofu Stir Fry.jpg': 'Spinach and Tofu Stir Fry',
            'Zucchini Noodles with Pesto.webp': 'Zucchini Noodles with Pesto',
            
            # Soups & Stews recipes
            'Chicken Stew with Vegetables.jpg': 'Chicken Stew with Vegetables',
            'Creamy Mushroom Soup.jpg': 'Creamy Mushroom Soup',
            'Lentil and Carrot Soup.jpg': 'Lentil and Carrot Soup',
            'Lentil Soup with Whole Wheat Bread.webp': 'Lentil Soup with Whole Wheat Bread',
            'Thai Coconut Curry Soup.jpeg': 'Thai Coconut Curry Soup',
            'Tom Yum Soup.jpg': 'Tom Yum Soup',
            'Tomato Basil Soup.jpg': 'Tomato Basil Soup',
            
            # Pasta & Noodles recipes
            'Japchae.jpg': 'Japchae',
            'Macaroni and Cheese.jpg': 'Macaroni and Cheese',
            'Pad Thai.jpg': 'Pad Thai',
            'Penne Arrabbiata.jpg': 'Penne Arrabbiata',
            'Pesto Fettuccine.webp': 'Pesto Fettuccine',
            
            # Rice-Based recipes
            'Bibimbap.webp': 'Bibimbap',
            'Jollof Rice.avif': 'Jollof Rice',
            'Mexican Burrito Bowl.jpg': 'Mexican Burrito Bowl',
            'Paella.jpeg': 'Paella',
            'Vegetarian Fried Rice.jpg': 'Vegetarian Fried Rice',
            
            # Snacks & Street Food recipes
            'Arancini.jpg': 'Arancini',
            'Empanadas.webp': 'Empanadas',
            'Falafel Balls.jpg': 'Falafel Balls',
            'French Fries with Truffle Aioli.jpg': 'French Fries with Truffle Aioli',
            'Tteokbokki.jpg': 'Tteokbokki',
            
            # Desserts recipes
            'Cheesecake.jpg': 'Cheesecake',
            'Chocolate Lava Cake.webp': 'Chocolate Lava Cake',
            'Gulab Jamun.webp': 'Gulab Jamun',
            'Mango Sticky Rice.jpg': 'Mango Sticky Rice',
            'Tiramisu.avif': 'Tiramisu',
            
            # Drinks recipes
            'Espresso Macchiato.png': 'Espresso Macchiato',
            'Fresh Lemon Mint Cooler.avif': 'Fresh Lemon Mint Cooler',
            'Iced Matcha Latte.webp': 'Iced Matcha Latte',
            'Lassi.webp': 'Lassi',
            'Masala Chai.webp': 'Masala Chai',
            'Mixed Berries Smoothie.jpg': 'Mixed Berries Smoothie',
        }

        media_path = os.path.join(settings.MEDIA_ROOT, 'recipes_images')
        
        if not os.path.exists(media_path):
            self.stdout.write(
                self.style.ERROR(f'Media directory {media_path} does not exist!')
            )
            return

        # Get list of existing image files
        existing_images = []
        for filename in os.listdir(media_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif')):
                existing_images.append(filename)

        self.stdout.write(f'Found {len(existing_images)} images in {media_path}')
        
        # Debug: Show all existing recipes
        all_recipes = Recipe.objects.all().values_list('title', flat=True)
        self.stdout.write(f'Available recipes: {", ".join(all_recipes)}')
        
        # Assign images to recipes
        assigned_count = 0
        for image_filename, recipe_title in image_mapping.items():
            try:
                # Find the recipe
                recipe = Recipe.objects.get(title=recipe_title)
                
                # Check if image file exists
                image_path = os.path.join(media_path, image_filename)
                if os.path.exists(image_path):
                    # Update recipe with the image
                    recipe.image = f'recipes_images/{image_filename}'
                    recipe.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Assigned {image_filename} to "{recipe_title}"')
                    )
                    assigned_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Image file {image_filename} not found for "{recipe_title}"')
                    )
                    
            except Recipe.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Recipe "{recipe_title}" not found for image {image_filename}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error assigning {image_filename} to "{recipe_title}": {str(e)}')
                )

        # Show unassigned images
        assigned_images = list(image_mapping.keys())
        unassigned_images = [img for img in existing_images if img not in assigned_images]
        
        if unassigned_images:
            self.stdout.write(
                self.style.WARNING(f'\n⚠️  Unassigned images: {", ".join(unassigned_images)}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully assigned {assigned_count} images to recipes!')
        ) 