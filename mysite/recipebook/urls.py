from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name='recipe_detail'),
    path("profile/", views.user_profile, name="user_profile"),
    path("like/<int:recipe_id>/", views.like_recipe, name='like_recipe'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]