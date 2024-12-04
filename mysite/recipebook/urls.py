from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('rate/<int:recipe_id>/', views.rate_recipe, name='rate_recipe')
]