from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Rating, UserProfile, Ingredient, Step
from django.forms import inlineformset_factory

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'register-new-form-control',
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'register-new-form-control',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'register-new-form-control',
                'placeholder': 'Confirm Password'
            }),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'category', 'cooking_time',
            'servings', 'image', 'is_featured', 'is_published'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'cooking_time': forms.NumberInput(attrs={'min': 1}),
            'servings': forms.NumberInput(attrs={'min': 1}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 0, 'step': '0.1'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['order', 'description', 'image']
        widgets = {
            'order': forms.NumberInput(attrs={'min': 1}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=True)
StepFormSet = inlineformset_factory(Recipe, Step, form=StepForm, extra=1, can_delete=True)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value', 'comment']
        widgets = {
            'value': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Share your thoughts about this recipe...'
            })
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'website', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://your-website.com'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your location'
            })
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Your Message'})) 