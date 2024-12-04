from django.contrib import admin
from .models import Recipe, Rating, LikedRecipe

# Recipe Admin
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'average_rating')
    list_filter = ('category', 'author', 'created_at')
    search_fields = ('title', 'ingredients', 'instructions')
    list_editable = ('category',)  # Allow editing category directly in the list view
    ordering = ('-created_at',)  # Order by created date, newest first
    fields = ('title', 'description', 'ingredients', 'instructions', 'author', 'category', 'image')  # Fields to display in form
    readonly_fields = ('created_at',)  # Make created_at field read-only

    def average_rating(self, obj):
        return obj.average_rating()
    average_rating.admin_order_field = 'average_rating'  # Allow sorting by average rating
    average_rating.short_description = 'Average Rating'

# Rating Admin
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'value', 'created_at')
    list_filter = ('value', 'user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__title')
    ordering = ('-created_at',)
    fields = ('user', 'recipe', 'value', 'created_at')
    readonly_fields = ('created_at',)

# LikedRecipe Admin
class LikedRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')
    list_filter = ('user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__title')
    ordering = ('-created_at',)
    fields = ('user', 'recipe', 'created_at')
    readonly_fields = ('created_at',)

# Register the models with their respective admin views
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(LikedRecipe, LikedRecipeAdmin)
