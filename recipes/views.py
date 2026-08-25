from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404

from .models import Recipe, Favorite
from .forms import RecipeForm, IngredientFormSetCreate, IngredientFormSetEdit

@login_required
def recipe_list(request):
    view_mode = request.GET.get("view", "mine")
    sort_mode = request.GET.get("sort", "newest")
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if view_mode == "all":
        recipes = Recipe.objects.filter(
            is_public=True
            ).exclude(
                owner=request.user
        )

    elif view_mode == "favorites" :
        recipes = Recipe.objects.filter(
            favorited_by__user=request.user
        ).filter(
            Q(owner=request.user) | Q(is_public=True)
        )
    
    else:
        recipes = Recipe.objects.filter(owner=request.user)

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(ingredients__name__icontains=query)
        ).distinct()

    if category:
        recipes = recipes.filter(category=category)

    recipes = recipes.prefetch_related("ingredients")

    if sort_mode == "oldest":
        recipes = recipes.order_by("created_at")
    else:
        recipes = recipes.order_by("-created_at")

    paginator = Paginator(recipes, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    favorite_recipe_ids = set(
        Favorite.objects.filter(user=request.user)
        .values_list("recipe_id", flat=True)
    )

    return render(
        request, 
        "recipes/recipe_list.html", 
        {
            "recipes": page_obj,
            "page_obj": page_obj,
            "view_mode": view_mode,
            "sort_mode": sort_mode,
            "query": query,
            "total_recipes": paginator.count,
            "favorite_recipe_ids": favorite_recipe_ids,
            "category": category,
            "category_choices": Recipe.CATEGORY_CHOICES,
        },
    )


@login_required
def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, owner=request.user)
    is_favorite = Favorite.objects.filter(
        user=request.user,
        recipe=recipe
    ).exists()
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe, "is_favorite": is_favorite})

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
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSetEdit(request.POST, instance=recipe)

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

@login_required
@require_POST
def toggle_favorite(request, slug):
    recipe = get_object_or_404(
        Recipe.objects.filter(Q(owner=request.user) | Q(is_public=True)),
        slug=slug
    )

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe,
    )

    if not created:
        favorite.delete()

    next_url = request.POST.get("next") or "recipes:list"
    return redirect(next_url)

@login_required
def recipe_public_list(request):
    recipes = Recipe.objects.filter(is_public=True).order_by("-created_at")
    return render(request,
                  "recipes/recipe_public_list.html",
                  {"recipes": recipes})

@login_required
def recipe_public_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, is_public=True)
    is_favorite = Favorite.objects.filter(
        user=request.user,
        recipe=recipe
    ).exists()
    return render(request, 
                  "recipes/recipe_public_detail.html", {"recipe": recipe, "is_favorite": is_favorite})

def placeholder_page(request):
    return render(request, "recipes/placeholder.html")