from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user_rating = None
    user_has_rated = recipe.ratings.filter(user=request.user).exists()

    if user_has_rated:
        user_rating = recipe.ratings.get(user=request.user).value

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        if 1 <= rating_value <= 5:
            Rating.objects.update_or_create(
                user=request.user,
                recipe=recipe,
                defaults={'value': rating_value}
            )
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'user_has_rated': user_has_rated,
        'user_rating': user_rating
    })

# User profile page showing liked recipes
@login_required
def user_profile(request):
    liked_recipes = LikedRecipe.objects.filter(user=request.user).select_related('recipe')

    if request.method == 'POST':
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if title and ingredients and instructions and category:
            Recipe.objects.create(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                category=category,
                image=image,
                author=request.user  # Assuming you have an `author` field in the Recipe model
            )
            messages.success(request, 'Your recipe has been created successfully!')
        else:
            messages.error(request, 'All fields are required to create a recipe.')

        return redirect('user_profile')

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
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
        else:
            # If the form is not valid, loop through its errors and display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        #messages.error(request, 'An error has occured. Please fill out the form and try again.')
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login a user
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')