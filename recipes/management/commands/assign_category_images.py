from django.core.management.base import BaseCommand
from recipes.models import Category
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Assigns existing images to their corresponding categories'

    def handle(self, *args, **kwargs):
        # Mapping of image filenames to category names
        image_mapping = {
            'Breakfast.jpeg': 'Breakfast',
            'Desserts.jpeg': 'Desserts',
            'Drinks.jpeg': 'Drinks',
            'healthy-vegetables.avif': 'Healthy & Vegetarian',
            'main-course.jpg': 'Main Course',
            'pasta-noodles.avif': 'Pasta & Noodles',
            'rice-based.jpeg': 'Rice-Based',
            'snacks-street-food.jpg': 'Snacks & Street Food',
            'soups-stews.avif': 'Soups & Stews',
        }

        media_path = os.path.join(settings.MEDIA_ROOT, 'category_images')
        
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
        
        # Assign images to categories
        assigned_count = 0
        for image_filename, category_name in image_mapping.items():
            try:
                # Find the category
                category = Category.objects.get(name=category_name)
                
                # Check if image file exists
                image_path = os.path.join(media_path, image_filename)
                if os.path.exists(image_path):
                    # Update category with the image
                    category.image = f'category_images/{image_filename}'
                    category.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Assigned {image_filename} to "{category_name}"')
                    )
                    assigned_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Image file {image_filename} not found for "{category_name}"')
                    )
                    
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Category "{category_name}" not found for image {image_filename}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error assigning {image_filename} to "{category_name}": {str(e)}')
                )

        # Show unassigned images (images in folder but not in mapping)
        assigned_images = list(image_mapping.keys())
        unassigned_images = [img for img in existing_images if img not in assigned_images]
        
        if unassigned_images:
            self.stdout.write(
                self.style.WARNING(f'\n⚠️  Unassigned images in folder: {", ".join(unassigned_images)}')
            )
            
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully assigned {assigned_count} images to categories!')
        ) 