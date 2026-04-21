from django.contrib import admin
from .models import Recipe, Ingredient


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title" , "prep_time_minutes", "created_at")
    inlines = [IngredientInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "recipe")
