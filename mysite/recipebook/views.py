from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe, Rating, LikedRecipe

# Index page showing all recipe
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', {'recipes': recipes})

# Recipe details page, users can rate the receipe
@login_required
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
            rating_value = int(request.POST.get('rating'))
            if 1 <= rating_value <= 5:
                Rating.objects.update_or_create(
                    user=request.user,
                    recipe=recipe,
                    defaults={'value': rating_value}
                )
            return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

# User profile page showing liked recipes
@login_required
def user_profile(request):
    liked_recipes = LikedRecipe.objects.filter(user=request.user)
    return render(request, 'recipes/user_profile.html', {'liked_recipes': liked_recipes})

# Add or remove a liked recipe
@login_required
def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    liked_recipe, created = LikedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        liked_recipe.delete()
    return redirect('index')

# Register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login a user
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'registration/login.html')