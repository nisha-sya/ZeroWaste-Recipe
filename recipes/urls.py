from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('splash/', views.splash, name='splash'),
    path('home/', views.home, name='home'),
    path('list/', views.recipe_list, name='recipe_list'),
    path('category/<slug:category_slug>/', views.category_recipes, name='category_recipes'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('<slug:slug>/edit/', views.edit_recipe, name='edit_recipe'),
    path('<slug:slug>/delete/', views.delete_recipe, name='delete_recipe'),
    path('<slug:slug>/favorite/', views.favorite_recipe, name='favorite_recipe'),
    path('<slug:slug>/', views.recipe_detail, name='recipe_detail'),
] 