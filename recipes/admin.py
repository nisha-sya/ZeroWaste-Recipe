from django.contrib import admin
from .models import Recipe, Category, Ingredient, Step, Rating, UserProfile

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class StepInline(admin.TabularInline):
    model = Step
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'cooking_time', 'difficulty', 'is_featured', 'is_published', 'created_at', 'views_count', 'average_rating')
    list_filter = ('category', 'difficulty', 'is_featured', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [IngredientInline, StepInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image', 'category', 'author')
        }),
        ('Recipe Details', {
            'fields': ('cooking_time', 'servings', 'difficulty')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Ratings & Views', {
            'fields': ('average_rating', 'views_count')
        }),
    )
    readonly_fields = ('views_count', 'average_rating', 'created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('recipe__title', 'user__username', 'comment')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website')
    search_fields = ('user__username', 'bio', 'location')
