from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("public/", views.recipe_public_list, name="public_list"),
    path("add/", views.recipe_create, name="create"),
    path("placeholder/", views.placeholder_page, name="placeholder"),
    path("public/<slug:slug>/", views.recipe_public_detail, name="public_detail"),
    
    path("<slug:slug>/edit/", views.recipe_update, name="update"),
    path("<slug:slug>/delete/", views.recipe_delete_confirm, name="recipe_delete_confirm"),
    path("<slug:slug>/delete/confirm/", views.recipe_delete, name="recipe_delete"),
    path("<slug:slug>/", views.recipe_detail, name="detail"),
    
    
    
]