from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Recipe
from .forms import RecipeForm, IngredientFormSetCreate, IngredientFormSetEdit

@login_required
def recipe_list(request):
    view_mode = request.GET.get("view", "mine")
    sort_mode = request.GET.get("sort", "newest")

    if view_mode == "public":
        recipes = Recipe.objects.filter(is_public=True)

    elif view_mode == "all":
        recipes = Recipe.objects.filter(
            Q(owner=request.user) | Q(is_public=True)
        )
    
    else:
        recipes = Recipe.objects.filter(owner=request.user)

    recipes = recipes.prefetch_related("ingredients")

    if sort_mode == "oldest":
        recipes = recipes.order_by("created_at")
    else:
        recipes = recipes.order_by("-created_at")

    return render(
        request, 
        "recipes/recipe_list.html", 
        {
            "recipes": recipes,
            "view_mode": view_mode,
            "sort_mode": sort_mode,
        },
    )

@login_required
def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, owner=request.user)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSetCreate(request.POST)
        
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()

            formset.instance = recipe
            formset.save()

            return redirect("recipes:detail", slug=recipe.slug)
        
    else:
        form = RecipeForm()
        formset = IngredientFormSetCreate()

    return render(
        request, "recipes/recipe_form.html", 
                  {"form": form, "formset": formset, "is_edit": False})

@login_required
def recipe_update(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, owner=request.user)

    if request.method =="POST":
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSetEdit(request.POST, request.FILES, instance=recipe)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("recipes:detail", slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSetEdit(instance=recipe)

    return render(
        request, "recipes/recipe_form.html", 
                  {"form": form, "formset": formset, "is_edit": True,
                   "recipe": recipe})

@login_required
def recipe_delete_confirm(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, owner=request.user)
    return render(
        request, "recipes/recipe_confirm_delete.html", {"recipe": recipe})

@login_required
@require_POST
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, owner=request.user)
    recipe.delete()
    return redirect("recipes:list")

def recipe_public_list(request):
    recipes = Recipe.objects.filter(is_public=True).order_by("-created_at")
    return render(request,
                  "recipes/recipe_public_list.html",
                  {"recipes": recipes})

def recipe_public_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, is_public=True)
    return render(request, 
                  "recipes/recipe_public_detail.html", {"recipe": recipe})

def placeholder_page(request):
    return render(request, "recipes/placeholder.html")