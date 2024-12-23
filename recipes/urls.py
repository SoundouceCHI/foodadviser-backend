from django.urls import path
from .views import get_recipe, get_recipes_list

urlpatterns = [
    path('<int:recipe_id>/', get_recipe, name='get_recipe'),  
    path('list/', get_recipes_list, name='get_recipes_list'),
]
