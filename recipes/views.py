from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Recipe, Category, Rating, UserProfile, Ingredient, Step
from .forms import RecipeForm, RatingForm, UserProfileForm, IngredientFormSet, StepFormSet, ContactForm
from django.contrib.auth import login
from .forms import RegistrationForm
from django.views.decorators.csrf import csrf_protect

def splash(request):
    return render(request, 'recipes/splash.html')

def home(request):
    featured_recipes = Recipe.objects.filter(is_featured=True)[:3]
    latest_recipes = Recipe.objects.order_by('-created_at')[:3]
    popular_recipes = Recipe.objects.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating')[:4]
    categories = Category.objects.all()
    
    context = {
        'featured_recipes': featured_recipes,
        'latest_recipes': latest_recipes,
        'popular_recipes': popular_recipes,
        'categories': categories,
    }
    return render(request, 'recipes/home.html', context)

def recipe_list(request):
    recipes = Recipe.objects.filter(is_published=True)
    categories = Category.objects.all()
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_id:
        recipes = recipes.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'recipes/recipe_list.html', context)

def category_recipes(request, category_slug):
    """View for browsing recipes by specific category"""
    category = get_object_or_404(Category, slug=category_slug)
    recipes = Recipe.objects.filter(category=category, is_published=True)
    
    # Pagination
    paginator = Paginator(recipes, 12)  # Show 12 recipes per page
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    # Get all categories for sidebar
    all_categories = Category.objects.all()
    
    context = {
        'category': category,
        'recipes': recipes,
        'all_categories': all_categories,
    }
    return render(request, 'recipes/category_recipes.html', context)

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    recipe.views_count += 1
    recipe.save()
    
    # Get related recipes
    related_recipes = Recipe.objects.filter(
        category=recipe.category,
        is_published=True
    ).exclude(id=recipe.id)[:3]
    
    # Check if user has favorited this recipe
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = recipe.favorites.filter(id=request.user.id).exists()
    
    # Handle rating submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()
            
            # Update recipe's average rating
            recipe.average_rating = recipe.ratings.aggregate(Avg('value'))['value__avg'] or 0
            recipe.save()
            
            messages.success(request, 'Your rating has been submitted!')
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        rating_form = RatingForm()
    
    context = {
        'recipe': recipe,
        'related_recipes': related_recipes,
        'rating_form': rating_form,
        'is_favorited': is_favorited,
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        step_formset = StepFormSet(request.POST, request.FILES, prefix='steps')
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            ingredient_formset.instance = recipe
            ingredient_formset.save()
            step_formset.instance = recipe
            step_formset.save()
            messages.success(request, 'Recipe added successfully!')
            return redirect('recipes:recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        step_formset = StepFormSet(prefix='steps')
    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
    })

@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(request.POST, request.FILES, instance=recipe, prefix='steps')
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            form.save()
            ingredient_formset.save()
            step_formset.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipes:recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(instance=recipe, prefix='steps')
    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe,
    })

@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipes:recipe_list')
    
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})

@login_required
@csrf_protect
def favorite_recipe(request, slug):
    # Debug: Print CSRF token info
    print(f"CSRF Token from cookie: {request.META.get('CSRF_COOKIE', 'Not found')}")
    print(f"CSRF Token from POST: {request.POST.get('csrfmiddlewaretoken', 'Not found')}")
    print(f"User: {request.user.username}")
    
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
        messages.info(request, 'Recipe removed from favorites.')
    else:
        recipe.favorites.add(request.user)
        messages.success(request, 'Recipe added to favorites!')
    return redirect('recipes:recipe_detail', slug=slug)

@login_required
def profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    user_recipes = Recipe.objects.filter(author=request.user)
    context = {
        'form': form,
        'user_recipes': user_recipes,
    }
    return render(request, 'recipes/profile.html', context)

@login_required
def dashboard(request):
    user_recipes = Recipe.objects.filter(author=request.user)
    recent_ratings = Rating.objects.filter(recipe__author=request.user).order_by('-created_at')[:5]
    
    context = {
        'user_recipes': user_recipes,
        'recent_ratings': recent_ratings,
    }
    return render(request, 'recipes/dashboard.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('recipes:contact')
    
    return render(request, 'recipes/contact.html')

def terms(request):
    return render(request, 'recipes/terms.html')

def privacy(request):
    return render(request, 'recipes/privacy.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
