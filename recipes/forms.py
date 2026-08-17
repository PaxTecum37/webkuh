from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", 
                  "description",
                  "category",
                  "instructions",
                  "prep_time_minutes",
                  "is_public",
                  "image",
                  ]

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", 
                  "amount",]

IngredientFormSetCreate = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=5,
    can_delete=True,
)

IngredientFormSetEdit = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=0,
    can_delete=True,
)