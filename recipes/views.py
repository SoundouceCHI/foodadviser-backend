from django.core.cache import cache
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from .models import Recipe, Nutrition

load_dotenv()

api_key = os.getenv('API_KEY')

def get_recipe(request, recipe_id):
    cache_key = f"recipe_{recipe_id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}&includeNutrition=true'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        cache.set(cache_key, data, timeout=3600)  # Cache the data for an hour
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to fetch recipe data"}, status=500)


def get_recipes_list(request):
    number = request.GET.get('number', 100)  

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&number={number}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    elif response.status_code == 402:
        return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)

    

def getRecipesSuggestionList(request): 
    ingredients = request.GET.get('list', '')
    number= int(request.GET.get('number', 8))
    print("Ingredients:", ingredients)
    print("Number:", number)

    if not ingredients:
            return JsonResponse({"error": "Missing 'list' parameter"}, status=400)
    
    url=(
            f'https://api.spoonacular.com/recipes/findByIngredients'
            f'?ingredients={ingredients}&number={number}&apiKey={api_key}'
        )
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    
    elif response.status_code == 402:
        return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)