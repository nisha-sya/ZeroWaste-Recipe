from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db.models import Avg
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, default='recipes/images/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes_images/', default='recipes/images/default.jpg')
    cooking_time = models.IntegerField(help_text='in minutes')
    servings = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    favorites = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)
    views_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Recipes'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_published']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['views_count']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['cooking_time']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['recipe']),
        ]

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_steps/', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['recipe', 'order']),
        ]
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order} for {self.recipe.title}"

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['recipe', 'user']),
            models.Index(fields=['value']),
            models.Index(fields=['created_at']),
        ]
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"{self.user.username}'s rating for {self.recipe.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.user.username}'s profile"
